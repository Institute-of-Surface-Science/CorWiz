import pandas as pd
import streamlit as st
import numpy as np
from .corrosion_model import corrosion_model


'''
    @article{Ali_2020, title={The empirical prediction of weight change and corrosion rate of low-carbon steel}, 
    volume={6}, 
    ISSN={2405-8440}, 
    url={http://dx.doi.org/10.1016/j.heliyon.2020.e05050}, 
    DOI={10.1016/j.heliyon.2020.e05050}, 
    number={9}, 
    journal={Heliyon}, 
    publisher={Elsevier BV}, 
    author={Ali, Nurdin and Fulazzaky, Mohamad Ali}, 
    year={2020}, 
    month=sep, 
    pages={e05050} }

'''

class empirical_prediction_model(corrosion_model):

    def __init__(self, parameters):
        corrosion_model.__init__(self)
        self.model_name = 'The empirical prediction of weight change and corrosion rate of low-carbon steel'
        self.article_identifier = ['ali2020']
        self.steel = "Low carbon steel"
        self.p = parameters

    
    def eval_material_loss(self, time):
        material_loss = (0.00006*self.p['C'] + 0.0008)*time + self.p['b']

        return material_loss
    

def get_constant_value(nacl_conc, table):
    nacl_concs = np.array(table.iloc[1:, 0].astype(int))
    constants = np.array(table.iloc[1:, 2].astype(float))
    # Check if the year is exactly in the data
    if nacl_conc in nacl_concs:
        return constants[nacl_concs == nacl_conc][0]
    else:
        # Interpolate the exponent value for the given year
        constant_value = np.interp(nacl_conc, nacl_concs, constants)
        return constant_value
    

def load_data(model_identifier):
    table_3 = pd.read_csv('../data/tables/' + model_identifier +'_tables_table_3.csv', header=None)

    return table_3


def get_input(symbol, limits):
    limit = limits[symbol]
    value = st.text_input(f"${symbol}$ - Enter {limit['desc']}  [ ${limit['unit']}$ ]:", value=limit['lower'])
    
    if value:
        try:
            value = float(value)
            if value < limit['lower'] or value > limit['upper']:
                st.error(f"Please enter a value between {limit['lower']} and {limit['upper']} ${limit['unit']}$")
            else:
                st.success(f"Value accepted: {value} ${limit['unit']}$")
        except ValueError:
            st.error("Please enter a valid number.")

    return float(value)


def get_parameters(limits):
    parameters = {}
    for symbol in limits.keys():
        parameters[symbol] = get_input(symbol, limits)

    return parameters


def display_formulas():
    st.write(r'Mass loss due to corrosion, $W_L [um] = (0.00006C + 0.0008)t + b $ ')


def IC_model_ali2020(model_identifier):
    time = st.number_input('Enter duration [years]:', min_value=1.0, max_value=100.0, step=0.1) 
    limits = {
        'C': {'desc': 'Concentration of NaCl', 'lower': 0, 'upper': 5, 'unit': '%w/w'},
    }
    parameters = get_parameters(limits)

    table_3 = load_data(model_identifier)

    parameters['b'] = get_constant_value(parameters['C'], table_3)

    display_formulas()
    return empirical_prediction_model(parameters), time