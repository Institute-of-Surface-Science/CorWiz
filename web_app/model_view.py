import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

from models import AC_model1, AC_model2, AC_model3, AC_model4, AC_model5, AC_model6, IC_model1


def display_model_info(model_info, model):
    st.write("Model developed by: " + model_info['model_developers'][model_info['model_names'].index(model)])
    st.write("Model Abstract: " + str(model_info['model_abstracts'][model_info['model_names'].index(model)]))
    try:
        st.write("Model Notes: " + model_info['model_special_notes'][model_info['model_names'].index(model)])
    except:
        pass


def run_model(model_id, model_identifier, model_functions):
    if model_id in model_functions:
        with st.container():
            model, time = model_functions[model_id](model_identifier)
    return model, time


def model_view(model_view_container):
    with model_view_container:
        st.write("---")
        st.header("Corrosion Mass Loss Models")

        atmospheric_corrosion_model_kadi_identifiers = pd.read_csv(
            '../data/atmospheric_corrosion_model_kadi_identifiers.csv')

        immersion_corrosion_model_kadi_identifiers = pd.read_csv(
            '../data/immersion_corrosion_model_kadi_identifiers.csv')

        columns = ['model_names', 'model_ids', 'model_kadi_identifiers', 'model_developers', 'model_abstracts',
                   'model_special_notes']
        AC_model_info = {col: atmospheric_corrosion_model_kadi_identifiers.iloc[:, idx].tolist() for idx, col in
                         enumerate(columns)}
        IC_model_info = {col: immersion_corrosion_model_kadi_identifiers.iloc[:, idx].tolist() for idx, col in
                         enumerate(columns)}

        models = ['Atmospheric corrosion models', 'Immersed corrosion models']
        ac_or_ic = st.selectbox(
            'Is your problem atmospheric corrosion or immersed corrosion?',
            models
        )

        if ac_or_ic == models[0]:
            model_info = AC_model_info
            model_functions = {1: AC_model1, 2: AC_model2, 3: AC_model3, 4: AC_model4, 5: AC_model5, 6: AC_model6}
        else:
            model_info = IC_model_info
            model_functions = {1: IC_model1}

        model = st.selectbox(
            'Please select model',
            model_info['model_names']
        )
        model_identifier = model_info['model_kadi_identifiers'][model_info['model_names'].index(model)]
        model_id = model_info['model_ids'][model_info['model_names'].index(model)]
        st.subheader("Selected model: " + model)

        image_column, data_column = st.columns((1, 1))
        fig = plt.figure(figsize=(10, 6))

        with data_column:
            display_model_info(model_info, model)
            model, time = run_model(model_id, model_identifier, model_functions)

        t = np.linspace(0, time, 400)
        D = model.eval_material_loss(t)
        plt.plot(t, D, color='blue')
        plt.xlabel(r'Time [years]')
        plt.ylabel(r'Mass loss $[um]$')
        plt.legend()
        plt.grid(True)

        with image_column:
            st.pyplot(fig)
