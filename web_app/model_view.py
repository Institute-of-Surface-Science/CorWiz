import numpy as np
import streamlit as st
import plotly.express as px
import streamlit.components.v1 as components
import json
import os

from models import *
from typing import Union, List

def display_model_info(model: Model) -> None:
    """Displays the model description and notes."""
    st.markdown(model.description)
    if model.special_note:
        st.markdown("#### Model Notes: \n" + model.special_note)

def load_corrosion_models_from_directory(directory_paths: Union[str, List[str]]) -> List[CorrosionModel]:
    """Loads all corrosion models from JSON files in the specified directory or directories.

    Args:
        directory_paths (Union[str, List[str]]): A single directory path or a list of directory paths.

    Returns:
        List[CorrosionModel]: A list of CorrosionModel instances loaded from the JSON files in the specified directory or directories.

    Raises:
        ValueError: If a directory does not exist or no JSON files are found.
    """
    # Mapping from identifiers to their respective corrosion model classes
    model_classes = {
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

    if isinstance(directory_paths, str):
        directory_paths = [directory_paths]  # Convert to a list for uniform processing

    corrosion_models = []
    for directory_path in directory_paths:
        if not os.path.isdir(directory_path):
            raise ValueError(f"The specified directory does not exist: {directory_path}")

        json_files = [os.path.join(directory_path, f) for f in os.listdir(directory_path) if f.endswith('.json')]
        if not json_files:
            raise ValueError(f"No JSON files found in the specified directory: {directory_path}")

        for json_file in json_files:
            try:
                # Load the JSON data
                with open(json_file, 'r', encoding='utf-8') as file:
                    data = json.load(file)

                # Determine the model identifier
                model_identifier = data.get('identifier', '')

                # Match the identifier with the corresponding class
                if model_identifier in model_classes:
                    corrosion_model = model_classes[model_identifier](json_file)
                    corrosion_models.append(corrosion_model)
                else:
                    print(f"Warning: No matching corrosion model class for identifier '{model_identifier}' in file {json_file}")

            except (ValueError, json.JSONDecodeError) as e:
                print(f"Warning: Error processing JSON file at {json_file}: {str(e)}")

    return corrosion_models

def plot_mass_loss_over_time(model, time_range):
    """Generates and embeds a Plotly figure for mass loss over time into Streamlit."""
    t = np.linspace(0, time_range, 400)
    D = model.evaluate_material_loss(t)

    fig = px.line(x=t, y=D, labels={'x': 'Time [years]', 'y': 'Mass loss [um]'}, title="Mass Loss Over Time",
                  height=700)

    plot_html = fig.to_html(full_html=False, include_plotlyjs='cdn')

    # Embed the figure in Streamlit using components.html since it doesn't work otherwise
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

    models = load_corrosion_models_from_directory(model_directories)

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
                selected_corrosion_type = st.selectbox('**Corrosion Type**', corrosion_types)

                filtered_models = [model for model, process_type in model_process_pairs if process_type == selected_corrosion_type]
                selected_model = st.selectbox('**Model**', filtered_models, format_func=lambda model: model.name + " (" + model.kadi_identifier + ")")

                time_range = st.number_input('Enter duration [years]:', min_value=2.5, max_value=100.0, step=2.5)

                selected_model.display_parameters()

            with plot_column:
                plot_mass_loss_over_time(selected_model, time_range)

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
