import pandas as pd
import streamlit as st
import numpy as np
from .corrosion_model import CorrosionModel


'''
    @article{hicks2012developing,
    title={Developing a risk assessment tool to predict the risk of accelerated corrosion to port infrastructure},
    author={Hicks, Randall E and Oster, Ryan J},
    journal={Great Lakes Maritime Research Institute},
    pages={1--20},
    year={2012}
    }
'''

class atmospheric_pollutant_and_ph_dependent_corrosion_r(CorrosionModel):

    def __init__(self, parameters, article_identifier):
        CorrosionModel.__init__(self)
        self.model_name = 'Corrosion modeling in marine structures'
        self.article_identifier = article_identifier
        self.steel = "A328 sheet steel"
        self.p = parameters

    
    def eval_material_loss(self, time):
        
        # Define the parameters and their formulas
        parameters = {
            'Alkalinity': (0.0014, -0.0103),
            'Chloride': (0.0055, 0.0382),
            'Sulfate': (0.0008, 0.0735),
            'Larson Skold Index': (0.0372, 0.0751),
            'Conductivity': (0.0004, 0.0052),
            'pH': (-0.0155, 0.2113),
            'Dissolved Organic Carbon': (0.0016, 0.0683),
            'Dissolved Copper': (3.785, 0.0803),
            'Dissolved Oxygen': (-0.0151, 0.2306),
        }

        # Calculate the d_ values
        d_values = {}
        for key, (multiplier, constant) in parameters.items():
            value = self.p[key]
            d_values[f'd_{key.replace(" ", "_")}'] = 0 if value == 0 else multiplier * value + constant

        # Example usage
        d_Alkalinity = d_values['d_Alkalinity']
        d_Chloride = d_values['d_Chloride']
        d_Sulfate = d_values['d_Sulfate']
        d_Larson_Skold_Index = d_values['d_Larson_Skold_Index']
        d_Conductivity = d_values['d_Conductivity']
        d_pH = d_values['d_pH']
        d_DOC = d_values['d_Dissolved_Organic_Carbon']
        d_DC = d_values['d_Dissolved_Copper']
        d_DO = d_values['d_Dissolved_Oxygen']

        corrosion_rate = d_Alkalinity + d_Chloride + d_Sulfate +d_Larson_Skold_Index + d_Conductivity + d_pH + d_DOC + d_DC + d_DO

        material_loss = corrosion_rate*time

        return material_loss


def IC_model_hicks2012(article_identifier):
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
    st.table(pd.read_csv('../data/tables/' + article_identifier + '_tables_table_2.csv'))
    st.title('Water quality measurements made from 9-10 August 2010 in the Duluth-Superior Harbor.')
    st.table(pd.read_csv('../data/tables/' + article_identifier + '_tables_table_7.csv'))
    st.title('Water quality measurements made from 26-27 July 2011 in the Duluth-Superior Harbor and three harbors on the north shore of Lake Superior.')
    st.table(pd.read_csv('../data/tables/' + article_identifier + '_tables_table_8.csv'))

    return atmospheric_pollutant_and_ph_dependent_corrosion_r(parameters, article_identifier), time
