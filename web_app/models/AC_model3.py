import pandas as pd
import streamlit as st
import numpy as np
from . atmospheric_corrosion_models import tropical_marine_env


def get_exponent_value(year, table):
    years = np.array(table[0].astype(int))
    exponents = np.array(table[1].astype(float))
    # Check if the year is exactly in the data
    if year in years:
        return exponents[years == year][0]
    else:
        # Interpolate the exponent value for the given year
        exponent_value = np.interp(year, years, exponents)
        return exponent_value
    

def load_data(model_identifier):
    table_1 = pd.read_csv('../data/tables/' + model_identifier +'_tables_table_1.csv', header=None)
    table_2 = pd.read_csv('../data/tables/' + model_identifier +'_tables_table_2.csv', header=None)

    return table_1, table_2


def get_corrosion_site(table_2):
    st.table(table_2)
    corrosion_site = st.selectbox('Select corrosion site:', ((table_2.iloc[1:, 0])))

    return table_2.iloc[1:, 0].tolist().index(corrosion_site)


def get_input(symbol, limits):
    limit = limits[symbol]
    value = st.text_input(f"Enter {limit['desc']} ({symbol}) [{limit['unit']}]:", value=limit['lower'])
    
    if value:
        try:
            value = float(value)
            if value < limit['lower'] or value > limit['upper']:
                st.error(f"Please enter a value between {limit['lower']} and {limit['upper']} {limit['unit']}.")
            else:
                st.success(f"Value accepted: {value} {limit['unit']}")
        except ValueError:
            st.error("Please enter a valid number.")

    return value


def AC_model3(model_identifier):
    time = st.number_input('Enter duration [years]:', min_value=1.0, max_value=100.0, step=0.1) 
    table_1, table_2 = load_data(model_identifier)
    parameters = {}
    parameters['corrosion_site'] = int(get_corrosion_site(table_2) + 1)
    limits = {'D': {'desc': 'Distance', 'lower': 25, 'upper': 375, 'unit': 'm'}}
    parameters['distance'] = get_input('D', limits)
    
    return tropical_marine_env(parameters), time
