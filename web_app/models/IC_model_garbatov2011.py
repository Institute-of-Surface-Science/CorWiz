import pandas as pd
import streamlit as st
import numpy as np
from .corrosion_model import corrosion_model


'''
    @article{garbatov2011corrosion,
    title={Corrosion modeling in marine structures},
    author={Garbatov, Y and Zayed, A and Soares, C Guedes},
    journal={Marine Technology and Engineering},
    year={2011}
    }
'''

class immersion_corrosion_predictive_model_incorporating(corrosion_model):

    def __init__(self, parameters, article_identifier):
        corrosion_model.__init__(self)
        self.model_name = 'Corrosion modeling in marine structures'
        self.article_identifier = article_identifier
        self.steel = "Mild carbon steel"
        self.p = parameters

    
    def eval_material_loss(self, time):
        
        d_Temperature = 0.0014*self.p['Temperature'] + 0.0154
        f_Temperature = self.p['Temperature']/15.5

        d_Dissolved_Oxygen = 0.0268*self.p['Dissolved Oxygen Concentration'] + 0.0086
        f_Dissolved_Oxygen = 0.9483*self.p['Dissolved Oxygen Concentration'] + 0.0517

        d_Flow_Velocity = 0.9338*(1 - np.exp(-0.4457*(self.p['Flow Velocity'] + 0.2817)))
        f_Flow_Velocity = 1.0978*(1 - np.exp(-2.2927*(self.p['Flow Velocity'] + 0.0548)))

        self.p['Nominal Corrosion Rate'] = d_Temperature + d_Dissolved_Oxygen + d_Flow_Velocity

        corrosion_rate = f_Temperature*f_Dissolved_Oxygen*f_Flow_Velocity*self.p['Nominal Corrosion Rate']

        material_loss = corrosion_rate*time

        return material_loss

def IC_model_garbatov2011(article_identifier):
    time = st.number_input('Enter duration [years]:', min_value=1.0, max_value=100.0, step=0.1) 

    parameters = {}
    
    parameters['Temperature'] = st.number_input('Enter the Temperature [°C]:', 0.1) 
    parameters['Dissolved Oxygen Concentration'] = st.number_input('Enter the Dissolved Oxygen [ml l^{-1}]:', 0.1) 
    parameters['Flow Velocity'] = st.number_input('Enter the Flow Velocity [m s^{-1}]:', 0.1) 

    return immersion_corrosion_predictive_model_incorporating(parameters, article_identifier), time
