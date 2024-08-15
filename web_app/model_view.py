import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
import json
from models import AC_model1, AC_model2, AC_model3, AC_model4, AC_model5, AC_model6, IC_model1, IC_model2
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
        'article_identifier' : []
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
            for item in extras:
                if item['key'] == 'Parameters':
                    model_infos['parameters'].append(item['value'])
                elif item['key'] == 'Formula':
                    model_infos['formulas'].append(item['value'])

    print(model_infos['kadi_identifiers'])

    return model_infos


def display_model_info(model_info, model):
    # st.markdown("#### Model developed by: \n" + model_info['model_developers'][model_info['model_names'].index(model)])
    st.markdown("#### Model Description: \n" + str(model_info['descriptions'][model_info['names'].index(model)]))
    try:
        st.markdown("#### Model Notes: \n" + model_info['special_notes'][model_info['names'].index(model)])
    except:
        pass


def run_model(model_identifier, model_functions, article_identifier):
    with st.container():
        model, time = model_functions[model_identifier](article_identifier)
    return model, time


def model_view(model_view_container):
    with model_view_container:
        st.write("---")
        st.header("Corrosion Mass Loss Models")

        immersion_corrosion_models = extract_model_details_from_json('../data/kadi4mat_json/immersion_corrosion_models/')
        atmospheric_corrosion_models = extract_model_details_from_json('../data/kadi4mat_json/atmospheric_corrosion_models/')

        models = ['Atmospheric corrosion models', 'Immersed corrosion models']
        ac_or_ic = st.selectbox(
            'Is your problem atmospheric corrosion or immersed corrosion?',
            models
        )

        if ac_or_ic == models[0]:
            model_info = atmospheric_corrosion_models
            model_functions = {'statistically-processed-atmospheric-corrosion-pred': AC_model1, 
                               'din-corrosion-protection-model-iso-9223-compliant': AC_model2, 
                               'marine-industrial-transition-corrosion-kinetics-mi': AC_model3, 
                               'exponential-corrosion-model-for-pollutant-concentr': AC_model4, 
                               'corrosion-degradation-model-including-coating-effe': AC_model5, 
                               'so2-cl-deposition-and-wetness-time-factor-based-ex': AC_model6}
        else:
            model_info = immersion_corrosion_models
            model_functions = {'chloride-influenced-low-carbon-steel-corrosion-pre': IC_model1, 
                               'thermo-nutrient-variability-steel-corrosion-model': IC_model2}  

        model = st.selectbox(
            'Please select model',
            model_info['names']
        )

        model_identifier = model_info['kadi_identifiers'][model_info['names'].index(model)]
        article_identifier = model_info['article_identifier'][model_info['names'].index(model)]
        st.subheader("Selected model: " + model)

        image_column, data_column = st.columns((1, 1))
        fig = plt.figure(figsize=(10, 6))

        with data_column:
            display_model_info(model_info, model)
            model, time = run_model(model_identifier, model_functions, article_identifier)

        if model is not None:
            t = np.linspace(0, time, 400)
            D = model.eval_material_loss(t)
            plt.plot(t, D, color='blue')
            plt.xlabel(r'Time [years]')
            plt.ylabel(r'Mass loss $[um]$')
            plt.legend()
            plt.grid(True)

            with image_column:
                st.pyplot(fig)
        else:
            st.write("No model selected.")
