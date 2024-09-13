import streamlit as st
import io
import pandas as pd
from models import *
from measurements import *
from typing import List
from plot_view import generate_plot, display_plot_html

# Mapping from identifiers to their respective corrosion model classes
corrosion_models = {
    'model_benarie1986': Benarie1986Model,
    'model_feliu1993': Feliu1993Model,
    'din-corrosion-protection-model-iso-9223-compliant': ISO9223Model,
    'model_klinesmith2007': KlineSmith2007Model,
    'model_ma2010': Ma2010Model,
    'model_soares1999': Soares1999Model,
    'model_ali2020': Ali2020Model,
    'model_garbatov2011': Garbatov2011Model,
    'model_hicks2012': Hicks2012Model,
    'model_kovalenko2016': Kovalenko2016Model,
}

def display_model_info(model: Model) -> None:
    """Display the model's description and any special notes."""
    st.markdown(model.description)
    if model.special_note:
        st.markdown(f"#### Model Notes:\n{model.special_note}")

def reset_plot():
    """Reset the plot data and regenerate the plot."""
    st.session_state.plot_data = []
    st.session_state.measurement_data = []
    return generate_plot(
        st.session_state.plot_data,
        st.session_state.selected_model,
        st.session_state.time_range,
        measurements=st.session_state.measurement_data
    )

def download_plot(key: str):
    """Provide a download button for the plot as a PNG image."""
    download_fig = generate_plot(
        st.session_state.plot_data,
        st.session_state.selected_model,
        st.session_state.time_range,
        width=1920,
        height=1080,
        measurements=st.session_state.measurement_data
    )
    buffer = io.BytesIO()
    download_fig.write_image(buffer, format="png")
    buffer.seek(0)
    st.download_button(
        label="Download plot as PNG",
        data=buffer,
        file_name="corrosion_plot.png",
        mime="image/png",
        key=key
    )

def display_model_selection_tab(models, model_process_types):
    """Display the Model Selection tab."""
    corrosion_types = sorted({process_type for _, process_type in model_process_types})
    selected_corrosion_type = st.selectbox('**Corrosion Type**', corrosion_types, key="corrosion_type")

    filtered_models = [
        model for model, process_type in model_process_types if process_type == selected_corrosion_type
    ]
    st.session_state.selected_model = st.selectbox(
        '**Model**', filtered_models,
        format_func=lambda model: f"{model.name} ({model.kadi_identifier.split('_')[-1]})",
        key="model_select"
    )

    st.number_input(
        'Enter duration [years]:', min_value=1.0, max_value=100.0, step=1.0, key="time_range"
    )

    st.session_state.selected_model.display_parameters()

    if st.session_state.selected_model.model_coordinates is not None:
        st.map(st.session_state.selected_model.model_coordinates)

    add_col, reset_col, download_col, _ = st.columns([1, 1, 1, 1])
    figure = generate_plot(
        st.session_state.plot_data,
        st.session_state.selected_model,
        st.session_state.time_range,
        measurements=st.session_state.measurement_data
    )

    with add_col:
        if st.button("Add Model to Plot", key="add_model_plot"):
            st.session_state.plot_data.append(st.session_state.selected_model)
            figure = generate_plot(
                st.session_state.plot_data,
                st.session_state.selected_model,
                st.session_state.time_range,
                measurements=st.session_state.measurement_data
            )

    with reset_col:
        if st.button("Reset Plot", key="reset_model_plot"):
            figure = reset_plot()

    with download_col:
        download_plot("model_download")

    return figure

def display_measurement_tab(measurements, figure):
    """Display the Measurement tab."""
    st.markdown("## Select a Measurement")

    measurement_names = [
        f"{measurement.name} ({measurement.kadi_identifier})" for measurement in measurements
    ]
    selected_measurement_name = st.selectbox("Select a measurement", measurement_names, key="measurement_select")

    selected_measurement = next(
        (measurement for measurement in measurements if
         f"{measurement.name} ({measurement.kadi_identifier})" == selected_measurement_name),
        None
    )

    if selected_measurement:
        st.markdown(f"### {selected_measurement.name}")
        st.markdown(f"**Description**: {selected_measurement.description}")

        add_col, reset_col, download_col, _ = st.columns([1, 1, 1, 1])

        with add_col:
            if st.button("Add Measurement to Plot", key="add_measurement_plot"):
                st.session_state.measurement_data.append(selected_measurement)
                figure = generate_plot(
                    st.session_state.plot_data,
                    st.session_state.selected_model,
                    st.session_state.time_range,
                    measurements=st.session_state.measurement_data
                )

        with reset_col:
            if st.button("Reset Plot", key="reset_measurement_plot"):
                figure = reset_plot()

        with download_col:
            download_plot("measurement_download")
        return figure
    else:
        return None

def display_wizard_tab(models, figure):
    """Display the Wizard tab."""
    material = st.selectbox('Select Material', ['Mild Steel'], key="wiz_material_select")
    has_coating = st.checkbox('Coating Applied', key="coating_checkbox")

    if has_coating:
        available_models = [model for model in models if model.kadi_identifier == 'model_soares1999']
    else:
        available_models = models

    if available_models:
        model_data = {
            'Model Name': [model.name for model in available_models],
            'Identifier': [model.kadi_identifier.split('_')[-1] for model in available_models]
        }
        model_df = pd.DataFrame(model_data)
        st.markdown("### Available Models:")
        st.table(model_df)
    else:
        st.markdown("No models available")

    add_col, reset_col, download_col, _ = st.columns([1, 1, 1, 1])

    with add_col:
        if st.button("Add Model to Plot", key="wizard_add_model"):
            st.session_state.plot_data.append(st.session_state.selected_model)
            figure = generate_plot(
                st.session_state.plot_data,
                st.session_state.selected_model,
                st.session_state.time_range,
                measurements=st.session_state.measurement_data
            )

    with reset_col:
        if st.button("Reset Plot", key="wizard_reset_plot"):
            figure = reset_plot()

    with download_col:
        download_plot("wizard_download")

    return figure

def display_model_view(page_container: st.container):
    """Display the model view interface for selecting and analyzing corrosion mass loss models.

    Args:
        page_container (st.container): The Streamlit container in which to display the interface.
    """
    # Load available corrosion models and measurements from directories
    model_directories = [
        '../data/kadi4mat_json/immersion_corrosion_models/',
        '../data/kadi4mat_json/atmospheric_corrosion_models/'
    ]
    models = load_corrosion_models_from_directory(model_directories, corrosion_models)

    measurement_directories = [
        '../data/kadi4mat_json/immersion_corrosion_measurements/',
    ]
    measurements = load_measurements_from_directory(measurement_directories)

    # Initialize session state variables
    if 'plot_data' not in st.session_state:
        st.session_state.plot_data = []
    if 'measurement_data' not in st.session_state:
        st.session_state.measurement_data = []
    if 'selected_model' not in st.session_state:
        st.session_state.selected_model = models[0]
    if 'time_range' not in st.session_state:
        st.session_state.time_range = 1.0

    figure = None

    with page_container:
        st.write("---")
        st.header("Corrosion Mass Loss Models")

        main_container, description_container = st.container(), st.container()
        model_process_types = get_corrosion_process_type(models)

        with main_container:
            plot_area, control_panel = st.columns((6, 4))

            with control_panel:
                model_tab, measurement_tab, wizard_tab = st.tabs(
                    ["Model Selection :books:", "Measurements :lab_coat:", "Wizard :sparkles:"]
                )

                with model_tab:
                    figure = display_model_selection_tab(models, model_process_types)

                with measurement_tab:
                    figure = display_measurement_tab(measurements, figure)

                with wizard_tab:
                    figure = display_wizard_tab(models, figure)

            with plot_area:
                if figure:
                    display_plot_html(figure)

        with description_container:
            description_expander = st.expander("**Model Description**", expanded=False)
            with description_expander:
                display_model_info(st.session_state.selected_model)

                st.write("### Model Formulas")
                if isinstance(st.session_state.selected_model.formula, list):
                    for formula in st.session_state.selected_model.formula:
                        st.markdown(f"**{formula['key']}**: {formula['value']}")
                elif isinstance(st.session_state.selected_model.formula, str):
                    st.markdown(st.session_state.selected_model.formula)
