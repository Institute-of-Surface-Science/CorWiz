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
    """Displays the model description and notes."""
    st.markdown(model.description)
    if model.special_note:
        st.markdown(f"#### Model Notes: \n{model.special_note}")


def reset_plot(selected_model, time_range):
    # Reset the list of models or measurements
    st.session_state.plot_data = []
    st.session_state.measurement_data = []
    return generate_plot(st.session_state.plot_data, selected_model, time_range,
                         measurements=st.session_state.measurement_data)


def download_plot(selected_model, time_range, key):
    download_fig = generate_plot(st.session_state.plot_data, selected_model, time_range, width=1920,
                                 height=1080, measurements=st.session_state.measurement_data)
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


def display_model_view(page_container):
    """
    Displays the model view interface for selecting and analyzing corrosion mass loss models.
    Args:
        page_container (st.container): The Streamlit container in which the model view interface will be displayed.
    """
    # Load available corrosion models from the directories
    model_directories = [
        '../data/kadi4mat_json/immersion_corrosion_models/',
        '../data/kadi4mat_json/atmospheric_corrosion_models/'
    ]
    models = load_corrosion_models_from_directory(model_directories, corrosion_models)

    measurement_directories = [
        '../data/kadi4mat_json/immersion_corrosion_measurements/',
    ]
    measurements = load_measurements_from_directory(measurement_directories)

    # Initialize plot_data in session state if it doesn't exist
    if 'plot_data' not in st.session_state:
        st.session_state.plot_data = []

    if 'measurement_data' not in st.session_state:
        st.session_state.measurement_data = []

    fig = None

    with page_container:
        st.write("---")
        st.header("Corrosion Mass Loss Models")

        main_content, description_content = st.container(), st.container()

        model_process_pairs = get_corrosion_process_type(models)

        with main_content:
            # Separate columns for plot and selection
            plot_column, selection_column = st.columns((6, 4))

            with selection_column:
                model_tab, measurement_tab, wizard_tab = st.tabs(
                    ["Model Selection :books:", "Measurements :lab_coat:", "Wizard :sparkles:"])

                # Model Selection Tab
                with model_tab:
                    # Selection for corrosion type
                    corrosion_types = sorted({process_type for _, process_type in model_process_pairs})
                    selected_corrosion_type = st.selectbox('**Corrosion Type**', corrosion_types, key="corrosion_type")

                    # Filter models based on the selected corrosion type
                    filtered_models = [
                        model for model, process_type in model_process_pairs if process_type == selected_corrosion_type
                    ]
                    selected_model = st.selectbox(
                        '**Model**', filtered_models,
                        format_func=lambda model: f"{model.name} (" + model.kadi_identifier.split("_")[-1] + ")",
                        key="model_select"
                    )

                    # Input for time range (duration in years)
                    time_range = st.number_input('Enter duration [years]:', min_value=1.0, max_value=100.0, step=1.0,
                                                 key="time_range")

                    # Display the selected model's parameters
                    selected_model.display_parameters()

                    # Display the location associated with the model on the map
                    if selected_model.model_coordinates is not None:
                        st.map(selected_model.model_coordinates)

                    # Create three columns for buttons to be side by side
                    add_button, reset_button, download_button, empty = st.columns([1, 1, 1, 1])
                    fig = generate_plot(st.session_state.plot_data, selected_model, time_range,
                                        measurements=st.session_state.measurement_data)

                    with add_button:
                        if st.button("Add Model to Plot", key="add_model_plot"):
                            st.session_state.plot_data.append(selected_model)
                            fig = generate_plot(st.session_state.plot_data, selected_model, time_range,
                                                measurements=st.session_state.measurement_data)

                    with reset_button:
                        if st.button("Reset Plot", key="reset_model_plot"):
                            fig = reset_plot(selected_model, time_range)

                    with download_button:
                        download_plot(selected_model, time_range, "model_download")
                # Measurement Tab
                with measurement_tab:
                    st.markdown("## Select a Measurement")

                    # Create a selectbox with the names of all available measurements
                    measurement_names = [f"{measurement.name} ({measurement.kadi_identifier})" for measurement in
                                         measurements]
                    selected_measurement_name = st.selectbox("Select a measurement", measurement_names)

                    # Find the selected measurement based on the selected name
                    selected_measurement = next(
                        (measurement for measurement in measurements if
                         f"{measurement.name} ({measurement.kadi_identifier})" == selected_measurement_name),
                        None
                    )

                    # Display the description of the selected measurement
                    if selected_measurement:
                        st.markdown(f"### {selected_measurement.name}")
                        st.markdown(f"**Description**: {selected_measurement.description}")

                        # Add to plot logic for measurement selection
                        add_button, reset_button, download_button, empty = st.columns([1, 1, 1, 1])

                        with add_button:
                            if st.button("Add Measurement to Plot", key="add_measurement_plot"):
                                st.session_state.measurement_data.append(selected_measurement)
                                fig = generate_plot(st.session_state.plot_data, selected_model, time_range,
                                                    measurements=st.session_state.measurement_data)

                        with reset_button:
                            if st.button("Reset Plot", key="reset_measurement_plot"):
                                fig = reset_plot(selected_model, time_range)

                        with download_button:
                            download_plot(selected_model, time_range, "measurement_download")

                with wizard_tab:
                    material = st.selectbox('Select Material', ['Mild Steel'], key="wiz_material_select")
                    has_coating = st.checkbox('Coating Applied', key="coating_checkbox")

                    # Dynamically filter the list of models based on the checkbox state
                    if has_coating:
                        available_models = [model for model in models if model.kadi_identifier == 'model_soares1999']
                    else:
                        available_models = models

                    # Prepare data for displaying as a table
                    if available_models:
                        model_data = {
                            'Model Name': [model.name for model in available_models],
                            'Identifier': [model.kadi_identifier.split("_")[-1] for model in available_models]
                        }

                        # Convert the dictionary into a DataFrame
                        model_df = pd.DataFrame(model_data)

                        # Display the DataFrame as a table in Streamlit
                        st.markdown("### Available Models:")
                        st.table(model_df)
                    else:
                        st.markdown("No models available")

                    # Display buttons to add the model to the plot or reset
                    add_button, reset_button, download_button, empty = st.columns([1, 1, 1, 1])

                    with add_button:
                        if st.button("Add Model to Plot", key="wizard_add_model"):
                            st.session_state.plot_data.append(selected_model)
                            fig = generate_plot(st.session_state.plot_data, selected_model, time_range,
                                                measurements=st.session_state.measurement_data)

                    with reset_button:
                        if st.button("Reset Plot", key="wizard_reset_plot"):
                            fig = reset_plot(selected_model, time_range)

                    with download_button:
                        download_plot(selected_model, time_range, "wizard_download")

            # Plot column displays the generated plot
            with plot_column:
                if fig:
                    display_plot_html(fig)

        with description_content:
            description_expander = st.expander("**Model Description**", expanded=False)
            with description_expander:
                display_model_info(selected_model)

                st.write("### Model Formulas")
                if isinstance(selected_model.formula, list):
                    for formula in selected_model.formula:
                        st.markdown(f"**{formula['key']}**: {formula['value']}")
                elif isinstance(selected_model.formula, str):
                    st.markdown(selected_model.formula)
