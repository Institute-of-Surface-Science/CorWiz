import pandas as pd
import streamlit as st
import numpy as np
from . immersed_corrosion_models import atmospheric_pollutant_and_ph_dependent_corrosion_r


def IC_model4(model_identifier):
    time = st.number_input('Enter duration [years]:', min_value=1.0, max_value=100.0, step=0.1) 
    
    parameters = {}
    
    parameters['Alkalinity'] = st.number_input(r'Enter the Alkalinity [$mg L^{-1}$]:', 0.1) 
    parameters['Chloride'] = st.number_input(r'Enter the Chloride content [$mg L^{-1}$]:', 0.1) 
    parameters['Sulfate'] = st.number_input(r'Enter the Sulfate content [$mg L^{-1}$]:', 0.1) 
    parameters['Larson Skold Index'] = st.number_input(r'Enter the Larson Skold Index:', 0.1) 
    parameters['Conductivity'] = st.number_input(r'Enter the Conductivity [$\mu D cm^{-1}$]:', 0.1) 
    parameters['pH'] = st.number_input(r'Enter the pH:', 0.1) 
    parameters['Dissolved Oxygen'] = st.number_input(r'Enter the Dissolved Oxygen content [$mg L^{-1}$]:', 0.1) 
    parameters['Dissolved Organic Carbon'] = st.number_input(r'Enter the Dissolved Organic Carbon content [$mg L^{-1}$]:', 0.1) 
    parameters['Dissolved Copper'] = st.number_input(r'Enter the Dissolved Copper content [$mg L^{-1}$]:', 0.1) 

    st.title('Statistical relationship between the long-term rate of steel corrosion (mm/yr) and various water quality parameters measured during 2010 at ten sites in the Duluth-Superior Harbor.')
    st.table(pd.read_csv('../data/tables/' + model_identifier + '_tables_table_2.csv'))
    st.title('Water quality measurements made from 9-10 August 2010 in the Duluth-Superior Harbor.')
    st.table(pd.read_csv('../data/tables/' + model_identifier + '_tables_table_7.csv'))
    st.title('Water quality measurements made from 26-27 July 2011 in the Duluth-Superior Harbor and three harbors on the north shore of Lake Superior.')
    st.table(pd.read_csv('../data/tables/' + model_identifier + '_tables_table_8.csv'))

    return atmospheric_pollutant_and_ph_dependent_corrosion_r(parameters), time
