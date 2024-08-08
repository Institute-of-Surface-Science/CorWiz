import streamlit as st

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from models import model1, model2, model3, model4, model5, model6

def model_view(model_view_container):
    with model_view_container:
        st.write("---")
        st.header("Corrosion Mass Loss Model")

        # Extract the model names and identifiers from the atmospheric_corrosion_model_kadi_identifiers.csv file

        atmospheric_corrosion_model_kadi_identifiers = pd.read_csv(
            '../data/atmospheric_corrosion_model_kadi_identifiers.csv')

        columns = ['model_names', 'model_ids', 'model_kadi_identifiers', 'model_developers', 'model_abstracts',
                   'model_special_notes']
        model_info = {col: atmospheric_corrosion_model_kadi_identifiers.iloc[:, idx].tolist() for idx, col in
                      enumerate(columns)}

        model = st.selectbox(
            'Please select model',
            ((model_info['model_names']))
        )
        model_identifier = model_info['model_kadi_identifiers'][model_info['model_names'].index(model)]
        model_id = model_info['model_ids'][model_info['model_names'].index(model)]
        st.subheader("Selected model: " + model)

        image_column, data_column, = st.columns((1, 1))
        fig = plt.figure(figsize=(10, 6))

        with data_column:
            st.write("Model developed by: " + model_info['model_developers'][model_info['model_names'].index(model)])
            st.write("Model Abstract: " + str(model_info['model_abstracts'][model_info['model_names'].index(model)]))
            try:
                st.write("Model Notes: " + model_info['model_special_notes'][model_info['model_names'].index(model)])
            except:
                pass

            if model_id == 1:
                with st.container():
                    model, time = model1(model_identifier)

            elif model_id == 2:
                with st.container():
                    model, time = model2(model_identifier)

            elif model_id == 3:
                with st.container():
                    model, time = model3(model_identifier)

            elif model_id == 4:
                with st.container():
                    model, time = model4(model_identifier)

            elif model_id == 5:
                with st.container():
                    model, time = model5(model_identifier)

            elif model_id == 6:
                with st.container():
                    model, time = model6(model_identifier)

            t = np.linspace(0, time, 400)
            D = model.eval_material_loss(t)
            plt.plot(t, D, color='blue')
            plt.xlabel(r'Time [years]')
            plt.ylabel(r'Mass loss $[um]$')
            plt.legend()
            plt.grid(True)

        with image_column:
            # # Save the figure
            # plt.savefig('../data/images/plot_output.png')
            # st.image("../data/images/plot_output.png")
            st.pyplot(fig)