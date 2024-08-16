import pandas as pd
import streamlit as st
import numpy as np
from . immersed_corrosion_models import thermo_nutrient_variability_steel_corrosion_model
    

def load_data(model_identifier):
    table_3 = pd.read_csv('../data/tables/' + model_identifier +'_tables_table_3.csv', header=None)

    return table_3


def IC_model2(model_identifier):
    time = st.number_input('Enter duration [years]:', min_value=1.0, max_value=100.0, step=0.1) 
    table_3 = load_data(model_identifier)
    st.table(table_3.iloc[:, 1:-2 ])

    parameters = {}

    parameters['Condition'] = int(st.selectbox('Select the Temperature and Dissolved Inorganic Nitrogen', (table_3.iloc[1:, 0])))

    parameters['c_s'] = float(table_3.iloc[parameters['Condition'], 3])
    parameters['r_s'] = float(table_3.iloc[parameters['Condition'], 4])
    
    return thermo_nutrient_variability_steel_corrosion_model(parameters), time
