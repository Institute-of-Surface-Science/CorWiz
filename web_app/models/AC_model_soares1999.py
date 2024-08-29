import streamlit as st
from .corrosion_model import corrosion_model
import numpy as np


'''
    @article{soares1999reliability,
    title={Reliability of maintained, corrosion protected plates subjected to non-linear corrosion and compressive loads},
    author={Soares, C Guedes and Garbatov, Yordan},
    journal={Marine structures},
    volume={12},
    number={6},
    pages={425--445},
    year={1999},
    publisher={Elsevier}
    }

'''

class coated_mass_loss_model(corrosion_model):

    def __init__(self, parameters, article_identifier):
        corrosion_model.__init__(self)
        self.model_name = 'Reliability of maintained, corrosion protected plates subjected to non-linear corrosion and compressive loads'
        self.article_identifier = article_identifier
        self.steel = "Steel"
        self.p = parameters

    
    def eval_material_loss(self, time):
        
        material_loss = np.zeros_like(time)  # Initialize the material_loss array with zeros
        mask = time >= self.p['t_c']  # Create a boolean mask for time elements >= T_c
        material_loss[mask] = self.p['d_inf'] * (1 - np.exp(-(time[mask] - self.p['t_c']) / self.p['t_t']))
        return material_loss
    

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


def AC_model_soares1999(article_identifier):
    time = st.number_input('Enter duration [years]:', min_value=1.0, max_value=100.0, step=0.1) 
    limits = {
        'd_inf': {'desc': 'Long term thickness of corrosion wastage', 'lower': 0.001, 'upper': 1000, 'unit': 'mm'},
        't_c': {'desc': 'Coating life', 'lower': 0, 'upper': 100, 'unit': 'years'},
        't_t': {'desc': 'Transition time', 'lower': 0, 'upper': 100, 'unit': 'years'}
    }
    parameters = get_parameters(limits)

    return coated_mass_loss_model(parameters, article_identifier), time
