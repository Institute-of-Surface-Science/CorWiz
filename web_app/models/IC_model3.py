import pandas as pd
import streamlit as st
import numpy as np
from . immersed_corrosion_models import immersion_corrosion_predictive_model_incorporating


def display_formulas():
    st.write(r'Mass loss due to corrosion, $W_L [um] = (0.00006C + 0.0008)t + b $ ')


def IC_model3(model_identifier):
    time = st.number_input('Enter duration [years]:', min_value=1.0, max_value=100.0, step=0.1) 
    

    parameters = {}
    
    parameters['Temperature'] = st.number_input('Enter the Temperature [°C]:', 0.1) 
    parameters['Dissolved Oxygen Concentration'] = st.number_input('Enter the Dissolved Oxygen [ml l^{-1}]:', 0.1) 
    parameters['Flow Velocity'] = st.number_input('Enter the Flow Velocity [m s^{-1}]:', 0.1) 

    return immersion_corrosion_predictive_model_incorporating(parameters), time
