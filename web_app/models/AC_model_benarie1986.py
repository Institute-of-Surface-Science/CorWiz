import pandas as pd
import streamlit as st
import numpy as np
from .corrosion_model import corrosion_model


'''
    @article{benarie1986general,
    title={A general corrosion function in terms of atmospheric pollutant concentrations and rain pH},
    author={Benarie, Michel and Lipfert, Frederick L},
    journal={Atmospheric Environment (1967)},
    volume={20},
    number={10},
    pages={1947--1958},
    year={1986},
    publisher={Elsevier}
    }
'''

class a_general_corrosion_function(corrosion_model):


    def __init__(self, parameters, article_identifier):
        corrosion_model.__init__(self)
        self.model_name = 'A general corrosion function in terms of atmospheric pollutant concentrations and rain pH'
        self.article_identifier = article_identifier
        self.steel = "Carbon Steel"
        self.p = parameters

    
    def eval_corrosion_speed_and_exponent(self):
        table_2 = pd.read_csv('../data/tables/' + self.article_identifier +'_tables_table_2.csv', header=None)
        A = float(table_2.iloc[self.p['corrosion_site'], 1])
        b = float(table_2.iloc[self.p['corrosion_site'], 2])

        return A, b 

    
    def eval_material_loss(self, time):
        A, n = self.eval_corrosion_speed_and_exponent()
        
        material_loss = A*time**n
        return material_loss
    

def load_data(article_identifier):

    return pd.read_csv('../data/tables/' + article_identifier +'_tables_table_2.csv', header=None)


def get_corrosion_site(table_2):
    corrosion_site = st.selectbox('Select corrosion site:', ((table_2.iloc[1:, 0])))

    return table_2.iloc[1:, 0].tolist().index(corrosion_site) + 1


def display_site_info(table_2, corrosion_site):
    st.write('Selected site: ' + table_2.iloc[corrosion_site, 0])
    st.write(r'Weight loss per wetness year, $A$ = ' + str(table_2.iloc[corrosion_site, 1]))
    st.write(r'Exponent, $b$ = ' + str(table_2.iloc[corrosion_site, 2]))
    st.write(r'$SO_2$ + $Cl^-$ deposits [$mg m^{-2} d^{-1}$] = ' + str(table_2.iloc[corrosion_site, 3]))
    st.write(r'$pH$ = ' + str(table_2.iloc[corrosion_site, 4]))


def AC_model_benarie1986(article_identifier):
    time = st.number_input('Enter duration [years]:', min_value=1.0, max_value=100.0, step=0.1) 
    table_2 = load_data(article_identifier)
    corrosion_site = get_corrosion_site(table_2)
    parameters = {'corrosion_site': int(corrosion_site)}
    display_site_info(table_2, corrosion_site)
    
    return a_general_corrosion_function(parameters, article_identifier), time
