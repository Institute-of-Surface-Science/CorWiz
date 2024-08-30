import pandas as pd
import streamlit as st
import numpy as np
from .corrosion_model import CorrosionModel


'''
    @article{ma2010atmospheric,
    title={The atmospheric corrosion kinetics of low carbon steel in a tropical marine environment},
    author={Ma, Yuantai and Li, Ying and Wang, Fuhui},
    journal={Corrosion Science},
    volume={52},
    number={5},
    pages={1796--1800},
    year={2010},
    publisher={Elsevier}
    }
'''

class tropical_marine_env(CorrosionModel):

    def __init__(self, parameters, article_identifier):
        CorrosionModel.__init__(self)
        self.model_name = 'The atmospheric corrosion kinetics of low carbon steel in a tropical marine environment'
        self.article_identifier = article_identifier
        self.steel = "Low Carbon Steel (Q235)"
        self.p = parameters

    
    def eval_corrosion_speed_and_exponent(self):
    # Define the distance points and their corresponding log(A) and n values
        distances = [25, 95, 375]
        
        # Site I values
        log_A_site_I = [0.13548, 0.52743, 0.44306]
        n_site_I = [2.86585, 2.18778, 1.55029]
        
        # Site II values
        log_A_site_II = [1.5095, 1.5981, 1.26836]
        n_site_II = [1.15232, 1.05915, 0.76748]
        
        # Select the site data
        if self.p['corrosion_site'] == 1:
            log_A_values = log_A_site_I
            n_values = n_site_I
        elif self.p['corrosion_site'] == 2:
            log_A_values = log_A_site_II
            n_values = n_site_II
        
        # Find the position for interpolation
        for i in range(len(distances) - 1):
            if distances[i] <= self.p['distance'] <= distances[i + 1]:
                # Linear interpolation for log(A)
                log_A = log_A_values[i] + (log_A_values[i + 1] - log_A_values[i]) * (self.p['distance'] - distances[i]) / (distances[i + 1] - distances[i])
                # Linear interpolation for n
                n = n_values[i] + (n_values[i + 1] - n_values[i]) * (self.p['distance'] - distances[i]) / (distances[i + 1] - distances[i])
                return np.exp(log_A), n
        
        # If the distance is exactly at one of the boundary points
        if self.p['distance'] == distances[0]:
            return np.exp(log_A_values[0]), n_values[0]
        elif self.p['distance'] == distances[-1]:
            return np.exp(log_A_values[-1]), n_values[-1]


    def eval_material_loss(self, time):

        A, n = self.eval_corrosion_speed_and_exponent()

        material_loss = A*time**n
        return material_loss
    

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
    

def load_data(article_identifier):
    table_1 = pd.read_csv('../data/tables/' + article_identifier +'_tables_table_1.csv', header=None)
    table_2 = pd.read_csv('../data/tables/' + article_identifier +'_tables_table_2.csv', header=None)

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


def AC_model_ma2010(article_identifier):
    time = st.number_input('Enter duration [years]:', min_value=1.0, max_value=100.0, step=0.1) 
    table_1, table_2 = load_data(article_identifier)
    parameters = {}
    parameters['corrosion_site'] = int(get_corrosion_site(table_2) + 1)
    limits = {'D': {'desc': 'Distance', 'lower': 25, 'upper': 375, 'unit': 'm'}}
    parameters['distance'] = get_input('D', limits)
    
    return tropical_marine_env(parameters, article_identifier), time
