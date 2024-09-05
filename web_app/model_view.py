import numpy as np
import streamlit as st
import plotly.express as px
import streamlit.components.v1 as components
import pandas as pd
import io
from models import *
from typing import Union, List

# Mapping from identifiers to their respective corrosion model classes
corwiz_models = {
    'model_benarie1986': Benarie1986Model,
    'model_feliu1993': Feliu1993Model,
    'din-corrosion-protection-model-iso-9223-compliant': ISO9223Model,
    'model_klinesmith2007': KlineSmith2007Model,
    'model_ma2010': Ma2010Model,
    'model_soares1999': Soares1999Model,
    'model_ali2020': Ali2010Model,
    'model_garbatov2011': Garbatov2011Model,
    'model_hicks2012': Hicks2012Model,
    'model_kovalenko2016': Kovalenko2016Model,
}

# Keep track of all models added for plotting
plot_data = []


def display_model_info(model: Model) -> None:
    """Displays the model description and notes."""
    st.markdown(model.description)
    if model.special_note:
        st.markdown("#### Model Notes: \n" + model.special_note)


def generate_plot(models, current_model, time_range):
    """Generates and returns a Plotly Express figure for mass loss over time."""
    t = np.linspace(0, time_range, 400)

    # Initialize a list for plotting
    plot_df = []

    # Plot the current model's data first
    D = current_model.evaluate_material_loss(t)
    current_model_data = pd.DataFrame(
        {'Time': t, 'Mass Loss': D, 'Model': f"{current_model.model_name} (live)"})
    plot_df.append(current_model_data)

    # Collect all y-values to check for max/min difference for log scaling
    all_y_values = [D]

    # Plot the additional models
    model_counter = 1
    for model in models:
        D = model.evaluate_material_loss(t)
        model_data = pd.DataFrame({'Time': t, 'Mass Loss': D, 'Model': f"{model.model_name} ({model_counter})"})
        plot_df.append(model_data)
        all_y_values.append(D)
        model_counter += 1

    # Combine all data into a single DataFrame
    plot_df = pd.concat(plot_df)

    # Flatten the list of y-values to check the ratio between max/min values
    all_y_values_flat = np.concatenate(all_y_values)

    # Filter out non-positive values to avoid errors with log scaling
    positive_y_values = all_y_values_flat[all_y_values_flat > 0]

    # Determine whether to use a log scale
    if len(positive_y_values) > 0:
        max_value = np.max(positive_y_values)
        min_value = np.min(positive_y_values)
        yaxis_type = "log" if max_value / min_value > 100 else "linear"
    else:
        yaxis_type = "linear"

    px.defaults.template = "plotly_white"

    # Plot using Plotly Express and use 'Model' for distinct colors and labels
    fig = px.line(
        plot_df,
        x='Time',
        y='Mass Loss',
        color='Model',  # Use 'Model' for coloring and labeling the lines
        labels={'Time': 'Time [years]', 'Mass Loss': 'Mass loss [um]'},
        title="Mass Loss Over Time",
        height=700
    )

    fig.update_layout(
        yaxis_type=yaxis_type,
        showlegend=True,  # Ensure the legend is displayed
        legend_title="Models"  # Properly label the legend
    )

    return fig


def display_plot_html(fig):
    """Displays the generated Plotly figure as HTML in Streamlit."""
    plot_html = fig.to_html(full_html=False, include_plotlyjs='cdn')
    components.html(
        f"""
        <div style="background-color: white; padding: 10px; border-radius: 10px;">
            {plot_html}
        </div>
        """,
        height=800,
        scrolling=True
    )

def display_model_view(container):
    """
    Displays the model view interface for selecting and analyzing corrosion mass loss models.

    Args:
        container (st.container): The Streamlit container in which the model view interface will be displayed.
    """
    model_directories = [
        '../data/kadi4mat_json/immersion_corrosion_models/',
        '../data/kadi4mat_json/atmospheric_corrosion_models/'
    ]

    models = load_corrosion_models_from_directory(model_directories, corwiz_models)

    global plot_data
    fig = None

    with container:
        st.write("---")
        st.header("Corrosion Mass Loss Models")

        main_content = st.container()
        description_content = st.container()

        model_process_pairs = get_corrosion_process_type(models)

        with main_content:
            plot_column, selection_column = st.columns((1, 1))

            with selection_column:
                corrosion_types = sorted({process_type for _, process_type in model_process_pairs})
                selected_corrosion_type = st.selectbox('**Corrosion Type**', corrosion_types,
                                                       key="corrosion_type_selectbox")

                filtered_models = [model for model, process_type in model_process_pairs if
                                   process_type == selected_corrosion_type]
                selected_model = st.selectbox(
                    '**Model**', filtered_models,
                    format_func=lambda model: model.name + " (" + model.kadi_identifier + ")", key="model_selectbox"
                )

                # Capture the time range input
                time_range = st.number_input('Enter duration [years]:', min_value=2.5, max_value=100.0, step=2.5,
                                             key="time_range_input")

                # Display parameters and compute corrosion speed and exponent using the selected time
                selected_model.display_parameters()

                # Display the location associated with the model on the map 
                if selected_model.MODEL_COORDINATES != None:
                    st.map(selected_model.MODEL_COORDINATES)

                # Create two columns for buttons to be side by side
                add_button, reset_button, download_button, empty = st.columns([1, 1, 1, 3])
                fig = generate_plot(plot_data, selected_model, time_range)

                with add_button:
                    if st.button("Add to Plot", key="add_button"):
                        plot_data.append(selected_model)  # Add the current model to the list of models to plot

                with reset_button:
                    if st.button("Reset Plot", key="reset_button"):
                        plot_data = []  # Reset the list of models

                with download_button:
                    if fig is not None:
                        buffer = io.BytesIO()
                        fig.write_image(buffer, format="png")
                        buffer.seek(0)

                        st.download_button(
                            label="Download plot as PNG",
                            data=buffer,
                            file_name="corrosion_plot.png",
                            mime="image/png"
                        )

            with plot_column:
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
