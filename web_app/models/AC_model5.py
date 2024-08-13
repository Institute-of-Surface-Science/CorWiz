import streamlit as st
from . atmospheric_corrosion_models import coated_mass_loss_model


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

    return float(value)


def get_parameters(limits):
    parameters = {}
    for symbol in limits.keys():
        parameters[symbol] = get_input(symbol, limits)

    return parameters


def AC_model5(model_identifier):
    time = st.number_input('Enter duration [years]:', min_value=1.0, max_value=100.0, step=0.1) 
    limits = {
        'd_inf': {'desc': 'Long term thickness of corrosion wastage', 'lower': 0.001, 'upper': 1000, 'unit': 'mm'},
        't_c': {'desc': 'Coating life', 'lower': 0, 'upper': 100, 'unit': 'years'},
        't_t': {'desc': 'Transition time', 'lower': 0, 'upper': 100, 'unit': 'years'}
    }
    parameters = get_parameters(limits)

    return coated_mass_loss_model(parameters), time
