import pandas as pd
import streamlit as st
import numpy as np
from .immersed_corrosion_models import immersed_corrosion_model
    

'''
    @article{Kovalenko_2016, 
    title={Long-term immersion corrosion of steel subject to large annual variations in seawater temperature and nutrient concentration}, 
    volume={13}, 
    ISSN={1744-8980}, 
    url={http://dx.doi.org/10.1080/15732479.2016.1229797}, 
    DOI={10.1080/15732479.2016.1229797}, 
    number={8}, 
    journal={Structure and Infrastructure Engineering}, 
    publisher={Informa UK Limited}, 
    author={Kovalenko, Roman and Melchers, Robert E. and Chernov, Boris}, 
    year={2016}, 
    month=sep, 
    pages={978–987} }

'''

class thermo_nutrient_variability_steel_corrosion_model(immersed_corrosion_model):

    def __init__(self, parameters):
        immersed_corrosion_model.__init__(self)
        self.model_name = 'Long-term immersion corrosion of steel subject to large annual variations in seawater temperature and nutrient concentration'
        self.article_identifier = ['kovalenko2016']
        self.steel = "Mild steel"
        self.p = parameters

    
    def eval_material_loss(self, time):
        material_loss = self.p['c_s'] + time*self.p['r_s']
        return material_loss


def load_data(model_identifier):
    table_3 = pd.read_csv('../data/tables/' + model_identifier +'_tables_table_3.csv', header=None)

    return table_3


def IC_model_kovalenko2016(model_identifier):
    time = st.number_input('Enter duration [years]:', min_value=1.0, max_value=100.0, step=0.1) 
    table_3 = load_data(model_identifier)
    st.table(table_3.iloc[:, 1:-2 ])

    parameters = {}

    parameters['Condition'] = int(st.selectbox('Select the Temperature and Dissolved Inorganic Nitrogen', (table_3.iloc[1:, 0])))

    parameters['c_s'] = float(table_3.iloc[parameters['Condition'], 3])
    parameters['r_s'] = float(table_3.iloc[parameters['Condition'], 4])
    
    return thermo_nutrient_variability_steel_corrosion_model(parameters), time
