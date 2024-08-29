import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
import streamlit as st
from streamlit_extras.stylable_container import stylable_container
import streamlit.components.v1 as components

from models import AC_model_fileu1993, AC_model_iso9223, AC_model_ma2010, AC_model_benarie1986, AC_model_soares1999, \
    AC_model_klinesmith2007, IC_model_ali2020, IC_model_kovalenko2016, IC_model_garbatov2011, IC_model_hicks2012
import os
import json


def extract_model_details_from_json(path):
    model_infos = {
        'names': [],
        'kadi_identifiers': [],
        'descriptions': [],
        'special_notes': [],
        'parameters': [],
        'formulas': [],
        'article_identifier': []
    }

    # Iterate over each file in the specified path
    for file_name in os.listdir(path):

        # model_info = [model name, kadi identifier, description, special notes, parameteres, formula]
        if file_name.endswith('.json'):
            json_file_path = os.path.join(path, file_name)

            with open(json_file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)

            # Access the 'extras' array in the JSON data
            model_infos['descriptions'].append(data.get('description', []))
            model_infos['names'].append(data.get('title', []))
            model_infos['kadi_identifiers'].append(data.get('identifier', []))
            model_infos['special_notes'].append(data.get('special notes', []))
            model_infos['article_identifier'].append(data.get('links', [])[0]['record_to']['identifier'])

            extras = data.get('extras', [])
            # Iterate through each model in the 'extras' array
            parameters_found = False
            formula_found = False
            for item in extras:
                if item['key'] == 'Parameters':
                    model_infos['parameters'].append(item['value'])
                    parameters_found = True
                if item['key'] == 'Formula':
                    model_infos['formulas'].append(item['value'])
                    formula_found = True
            if not parameters_found:
                model_infos['parameters'].append('')
            if not formula_found:
                model_infos['formulas'].append('')

    return model_infos


def display_model_info(model_info, model):
    # st.markdown("#### Model developed by: \n" + model_info['model_developers'][model_info['model_names'].index(model)])
    st.markdown(str(model_info['descriptions'][model_info['names'].index(model)]))
    try:
        st.markdown("#### Model Notes: \n" + model_info['special_notes'][model_info['names'].index(model)])
    except:
        pass


def run_model(model_identifier, model_functions, article_identifier):
    with st.container():
        model, time = model_functions[model_identifier](article_identifier)
    return model, time


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
                model_categories = ['Atmospheric corrosion models', 'Immersed corrosion models']

                model_category_selection = st.selectbox('**Corrosion Type**', model_categories)

                if model_category_selection == 'Atmospheric corrosion models':
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
                article_identifier = model_info['article_identifier'][model_info['names'].index(selected_model_name)]
                formulas = model_info['formulas'][model_info['names'].index(selected_model_name)]

                model, time = run_model(model_identifier, model_functions, article_identifier)

            if model is not None:
                t = np.linspace(0, time, 400)
                D = model.eval_material_loss(t)

                fig = px.line(x=t, y=D, labels={'x': 'Time [years]', 'y': 'Mass loss [um]'},
                              title="Mass Loss Over Time", height=700)

                with image_column:
                    chart_container = st.container()
                    plot_html = fig.to_html(full_html=False, include_plotlyjs='cdn')

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
            else:
                st.write("No model selected.")
        with description_box:
            description = st.expander("**Model Description**", expanded=False)

            with description:
                display_model_info(model_info, selected_model_name)

                st.write("### Model Formulas")
                for formula in formulas:
                    st.write(r'' + formula['key'] + ': ' + formula['value'])
