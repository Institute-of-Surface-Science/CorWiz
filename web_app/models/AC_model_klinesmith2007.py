import streamlit as st
import pandas as pd
from .corrosion_model import corrosion_model
import numpy as np


'''
    @article{klinesmith2007effect,
    title={Effect of environmental conditions on corrosion rates},
    author={Klinesmith, Dawn E and McCuen, Richard H and Albrecht, Pedro},
    journal={Journal of Materials in Civil Engineering},
    volume={19},
    number={2},
    pages={121--129},
    year={2007},
    publisher={American Society of Civil Engineers}
    }
'''

class sophisticated_corrosion_rate(corrosion_model):

    def __init__(self, parameters, article_identifier):
        corrosion_model.__init__(self)
        self.model_name = 'Effect of environmental conditions on corrosion rates'
        self.article_identifier = article_identifier
        self.steel = "Carbon Steel"
        self.p = parameters

    
    def eval_material_loss(self, time):
        
        table_2 = pd.read_csv('../data/tables/' + self.article_identifier +'_tables_table_2.csv', header=None)
        A = float(table_2.iloc[1, 2])
        B = float(table_2.iloc[1, 3])
        C = float(table_2.iloc[1, 4])
        D = float(table_2.iloc[1, 5])
        E = float(table_2.iloc[1, 6])
        F = float(table_2.iloc[1, 7])
        G = float(table_2.iloc[1, 8])
        H = float(table_2.iloc[1, 9])
        J = float(table_2.iloc[1, 10])
        T0 = float(table_2.iloc[1, 11])

        material_loss = A*(time**B)*((self.p['TOW']*365*24/C)**D)*(1+(self.p['SO2']/E)**F)*(1+(self.p['Cl']/G)**H)*(np.exp(J*(self.p['T']+T0)))
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

def AC_model_klinesmith2007(article_identifier):
    time = st.number_input('Enter duration [years]:', min_value=1.0, max_value=100.0, step=0.1) 
    limits = {
        'T': {'desc': 'Temperature', 'lower': -17.1, 'upper': 28.7, 'unit': '°C'},
        'TOW': {'desc': 'Time of wetness', 'lower': 0, 'upper': 1, 'unit': 'annual fraction'},
        'SO2': {'desc': 'SO₂-Deposit', 'lower': 0.7, 'upper': 150.4, 'unit': 'mg/(m²⋅d)'},
        'Cl': {'desc': 'Cl⁻-Deposit', 'lower': 0.4, 'upper': 760.5, 'unit': 'mg/(m²⋅d)'}
    }
    parameters = get_parameters(limits)

    return sophisticated_corrosion_rate(parameters, article_identifier), time
