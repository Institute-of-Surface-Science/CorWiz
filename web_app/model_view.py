import os
import json
import numpy as np
import streamlit as st
import plotly.express as px
import streamlit.components.v1 as components

from models import (
    AC_model_fileu1993, AC_model_iso9223, AC_model_ma2010,
    AC_model_benarie1986, AC_model_soares1999, AC_model_klinesmith2007,
    IC_model_ali2020, IC_model_kovalenko2016, IC_model_garbatov2011,
    IC_model_hicks2012
)


def extract_model_details_from_json(directory_path):
    """Extracts model details from JSON files in the specified directory."""
    model_details = {
        'names': [],
        'kadi_identifiers': [],
        'descriptions': [],
        'special_notes': [],
        'parameters': [],
        'formulas': [],
        'article_identifiers': []
    }

    for file_name in os.listdir(directory_path):
        if file_name.endswith('.json'):
            json_file_path = os.path.join(directory_path, file_name)
            with open(json_file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)

            model_details['names'].append(data.get('title', ''))
            model_details['kadi_identifiers'].append(data.get('identifier', ''))
            model_details['descriptions'].append(data.get('description', ''))
            model_details['special_notes'].append(data.get('special notes', ''))
            model_details['article_identifiers'].append(data.get('links', [{}])[0].get('record_to', {}).get('identifier', ''))

            extras = data.get('extras', [])
            parameters = next((item['value'] for item in extras if item['key'] == 'Parameters'), '')
            formula = next((item['value'] for item in extras if item['key'] == 'Formula'), '')

            model_details['parameters'].append(parameters)
            model_details['formulas'].append(formula)

    return model_details


def display_model_info(model_info, model_name):
    # st.markdown("#### Model developed by: \n" + model_info['model_developers'][model_info['model_names'].index(model)])
    st.markdown(str(model_info['descriptions'][model_info['names'].index(model_name)]))
    try:
        st.markdown("#### Model Notes: \n" + model_info['special_notes'][model_info['names'].index(model_name)])
    except:
        pass


def run_model(model_identifier, model_functions, article_identifier):
    return  model_functions[model_identifier](article_identifier)

def plot_mass_loss_over_time(model, time_range):
    """Generates and returns a Plotly figure for mass loss over time."""
    t = np.linspace(0, time_range, 400)
    D = model.eval_material_loss(t)
    fig = px.line(x=t, y=D, labels={'x': 'Time [years]', 'y': 'Mass loss [um]'}, title="Mass Loss Over Time", height=700)
    return fig


def model_view(model_view_container):
    immersion_corrosion_models = extract_model_details_from_json('../data/kadi4mat_json/immersion_corrosion_models/')
    atmospheric_corrosion_models = extract_model_details_from_json(
        '../data/kadi4mat_json/atmospheric_corrosion_models/')

    with model_view_container:
        st.write("---")
        st.header("Corrosion Mass Loss Models")

        main_view = st.container()
        description_box = st.container()
        model_info = None
        selected_model_name = None

        with main_view:
            image_column, data_column = st.columns((1, 1))
            with data_column:
                model_categories = ['Atmospheric corrosion', 'Immersion corrosion']

                model_category_selection = st.selectbox('**Corrosion Type**', model_categories)

                if model_category_selection == 'Atmospheric corrosion':
                    model_info = atmospheric_corrosion_models
                    model_functions = {'model_feliu1993': AC_model_fileu1993,
                                       'din-corrosion-protection-model-iso-9223-compliant': AC_model_iso9223,
                                       'model_ma2010': AC_model_ma2010,
                                       'model_benarie1986': AC_model_benarie1986,
                                       'model_soares1999': AC_model_soares1999,
                                       'model_klinesmith2007': AC_model_klinesmith2007}
                else:
                    model_info = immersion_corrosion_models
                    model_functions = {'model_ali2020': IC_model_ali2020,
                                       'model_kovalenko2016': IC_model_kovalenko2016,
                                       'model_garbatov2011': IC_model_garbatov2011,
                                       'model_hicks2012': IC_model_hicks2012}

                selected_model_name = st.selectbox('**Model**', model_info['names'])

                model_identifier = model_info['kadi_identifiers'][model_info['names'].index(selected_model_name)]
                article_identifier = model_info['article_identifiers'][model_info['names'].index(selected_model_name)]
                formulas = model_info['formulas'][model_info['names'].index(selected_model_name)]

                model, time = run_model(model_identifier, model_functions, article_identifier)

            with image_column:
                chart_container = st.container()
                plot_html = plot_mass_loss_over_time(model, time).to_html(full_html=False, include_plotlyjs='cdn')

                with chart_container:
                    components.html(
                        f"""
                           <div style="background-color: white; padding: 10px; border-radius: 10px;">
                               {plot_html}
                           </div>
                           """,
                        height=800,
                        scrolling=True
                    )

        with description_box:
            description = st.expander("**Model Description**", expanded=False)

            with description:
                display_model_info(model_info, selected_model_name)

                st.write("### Model Formulas")
                for formula in formulas:
                    st.write(r'' + formula['key'] + ': ' + formula['value'])
