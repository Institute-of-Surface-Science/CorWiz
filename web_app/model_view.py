
import numpy as np
import streamlit as st
import plotly.express as px
import streamlit.components.v1 as components

from models import *

def display_model_info(model: Model) -> None:
    """Displays the model description and notes."""
    st.markdown(model.description)
    if model.special_note:
        st.markdown("#### Model Notes: \n" + model.special_note)


def run_model(model_identifier: str):
    """Runs the selected model using the provided identifier."""
    model_functions = {
        'model_feliu1993': AC_model_fileu1993,
        'din-corrosion-protection-model-iso-9223-compliant': AC_model_iso9223,
        'model_ma2010': AC_model_ma2010,
        'model_benarie1986': AC_model_benarie1986,
        'model_soares1999': AC_model_soares1999,
        'model_klinesmith2007': AC_model_klinesmith2007,
        'model_ali2020': IC_model_ali2020,
        'model_kovalenko2016': IC_model_kovalenko2016,
        'model_garbatov2011': IC_model_garbatov2011,
        'model_hicks2012': IC_model_hicks2012
    }

    # TODO: remove this crap
    if model_identifier == 'din-corrosion-protection-model-iso-9223-compliant':
        article_identifier = 'din-en-iso-92232012-05'
    else:
        # Extract the article identifier from the model identifier
        article_identifier = model_identifier.split("_")[1]

    return model_functions[model_identifier](article_identifier)


def plot_mass_loss_over_time(model, time_range):
    """Generates and embeds a Plotly figure for mass loss over time into Streamlit."""
    t = np.linspace(0, time_range, 400)
    D = model.eval_material_loss(t)

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


def model_view(model_view_container):
    """Main function to display the model view."""
    directories = [
        '../data/kadi4mat_json/immersion_corrosion_models/',
        '../data/kadi4mat_json/atmospheric_corrosion_models/'
    ]
    models = load_models_from_directory(directories)

    with model_view_container:
        st.write("---")
        st.header("Corrosion Mass Loss Models")

        main_view = st.container()
        description_box = st.container()

        # Get all process types for the first selector box
        model_process_types = get_corrosion_process_type(models)

        with main_view:
            image_column, data_column = st.columns((1, 1))
            with data_column:
                # Get unique, sorted corrosion process types
                model_categories = sorted({process_type for _, process_type in model_process_types})

                model_category_selection = st.selectbox('**Corrosion Type**', model_categories)

                # Filter models by the corrosion type selection
                filtered_models = [model for model, process_type in model_process_types if
                                   process_type == model_category_selection]
                selected_model = st.selectbox('**Model**', filtered_models, format_func=lambda model: model.name)
                model, time = run_model(selected_model.kadi_identifier)

            with image_column:
                chart_container = st.container()

                with chart_container:
                    plot_mass_loss_over_time(model, time)

            with description_box:
                description = st.expander("**Model Description**", expanded=False)

                with description:
                    display_model_info(selected_model)

                    st.write("### Model Formulas")
                    if isinstance(selected_model.formula, list):
                        for formula in selected_model.formula:
                            st.markdown(f"**{formula['key']}**: {formula['value']}")
                    elif isinstance(selected_model.formula, str):
                        st.markdown(selected_model.formula)