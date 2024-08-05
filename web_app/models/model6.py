import pandas as pd
import streamlit as st
import numpy as np
from . atmospheric_corrosion_models import sophisticated_corrosion_rate

def get_input(limits, symbol):
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

def model6(model_identifier):

    time = st.number_input('Enter duration [years]:', min_value=1.0, max_value=100.0, step=0.1) 
    
    parameters = {}

    limits = {
        'T': {'desc': 'Temperature', 'lower': -17.1, 'upper': 28.7, 'unit': '°C'},
        'TOW': {'desc': 'Time of wetness', 'lower': 1, 'upper': 365, 'unit': 'days/Year'},
        'SO2': {'desc': 'SO₂-Deposit', 'lower': 0.7, 'upper': 150.4, 'unit': 'mg/(m²⋅d)'},
        'Cl': {'desc': 'Cl⁻-Deposit', 'lower': 0.4, 'upper': 760.5, 'unit': 'mg/(m²⋅d)'}
        }

    for symbol in limits.keys():
        parameters[symbol] = float(get_input(limits, symbol))

    return sophisticated_corrosion_rate(parameters), time