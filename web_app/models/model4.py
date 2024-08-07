import pandas as pd
import streamlit as st
import numpy as np
from . atmospheric_corrosion_models import a_general_corrosion_function


def model4(model_identifier):


    time = st.number_input('Enter duration [years]:', min_value=1.0, max_value=100.0, step=0.1) 

    table_2 = pd.read_csv('../data/tables/' + model_identifier +'_tables_table_2.csv', header=None)

    corrosion_site = st.selectbox(
    'Select corrosion site:',
    ((table_2.iloc[1:, 0]))
    )
    corrosion_site = table_2.iloc[1:, 0].tolist().index(corrosion_site) + 1
    parameters = {}
    parameters['corrosion_site'] = int(corrosion_site)

    st.write('Selected site: ' + table_2.iloc[corrosion_site, 0])
    st.write(r'Weight loss per wetness year, A = ' + str(table_2.iloc[corrosion_site, 1]))
    st.write(r'Exponent, b = ' + str(table_2.iloc[corrosion_site, 2]))
    st.write(r'SO_2 + CL^- deposits [mg m^{-2} d^{-1}] = ' + str(table_2.iloc[corrosion_site, 3]))
    st.write(r'pH = ' + str(table_2.iloc[corrosion_site, 4]))
    return a_general_corrosion_function(parameters), time