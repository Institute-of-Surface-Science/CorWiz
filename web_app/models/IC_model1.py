import pandas as pd
import streamlit as st
import numpy as np
from . immersed_corrosion_models import empirical_prediction_model


def get_constant_value(nacl_conc, table):
    nacl_concs = np.array(table.iloc[1:, 0].astype(int))
    constants = np.array(table.iloc[1:, 2].astype(float))
    # Check if the year is exactly in the data
    if nacl_conc in nacl_concs:
        return constants[nacl_concs == nacl_conc][0]
    else:
        # Interpolate the exponent value for the given year
        constant_value = np.interp(nacl_conc, nacl_concs, constants)
        return constant_value
    

def load_data(model_identifier):
    table_3 = pd.read_csv('../data/tables/' + model_identifier +'_tables_table_3.csv', header=None)

    return table_3


def get_input(symbol, limits):
    limit = limits[symbol]
    value = st.text_input(f"${symbol}$ - Enter {limit['desc']}  [ ${limit['unit']}$ ]:", value=limit['lower'])
    
    if value:
        try:
            value = float(value)
            if value < limit['lower'] or value > limit['upper']:
                st.error(f"Please enter a value between {limit['lower']} and {limit['upper']} ${limit['unit']}$")
            else:
                st.success(f"Value accepted: {value} ${limit['unit']}$")
        except ValueError:
            st.error("Please enter a valid number.")

    return float(value)


def get_parameters(limits):
    parameters = {}
    for symbol in limits.keys():
        parameters[symbol] = get_input(symbol, limits)

    return parameters


def display_formulas():
    st.write(r'Mass loss due to corrosion, $W_L [um] = (0.00006C + 0.0008)t + b $ ')


def IC_model1(model_identifier):
    time = st.number_input('Enter duration [years]:', min_value=1.0, max_value=100.0, step=0.1) 
    limits = {
        'C': {'desc': 'Concentration of NaCl', 'lower': 0, 'upper': 5, 'unit': '%w/w'},
    }
    parameters = get_parameters(limits)

    table_3 = load_data(model_identifier)

    parameters['b'] = get_constant_value(parameters['C'], table_3)

    display_formulas()
    print(parameters)
    return empirical_prediction_model(parameters), time
