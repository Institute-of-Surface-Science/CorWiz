import pandas as pd
import streamlit as st
from .corrosion_model import corrosion_model
import numpy as np


'''
    @article{feliu1993prediction,
    title={I_The prediction of atmospheric corrosion from meteorological and pollution parameters—I. Annual corrosion},
    author={Feliu, S and Morcillo, Manuel and Feliu Jr, S},
    journal={Corrosion Science},
    volume={34},
    number={3},
    pages={403--414},
    year={1993},
    publisher={Elsevier}
'''

class i_the_prediction_of_atmospheric_corrosion_from_met(corrosion_model):
   
    def __init__(self, parameters):
        corrosion_model.__init__(self)
        self.model_name = 'The prediction of atmospheric corrosion from meteorological and pollution parameters—I. Annual corrosion'
        self.article_identifier = ['feliu1993']
        self.steel = "Carbon Steel"
        self.p = parameters


    def eval_annual_corrosion(self):

        if self.p['Binary Interaction']:
            annual_corrosion = (132.4 * self.p['Chloride pollution annual average'] * 
                        (1 + 0.038 * self.p['Temperature'] - 
                         1.96 * self.p['Wetness time'] - 
                         0.53 * self.p['SO2 pollution annual average'] + 
                         74.6 * self.p['Wetness time'] * (1 + 1.07 * self.p['SO2 pollution annual average']) - 
                         6.3))
        else:
            annual_corrosion = (33.0 + 
                        57.4 * self.p['Chloride pollution annual average'] + 
                        26.6 * self.p['SO2 pollution annual average'])

        return annual_corrosion
    

    def evaluate_exponent(self):
        table_4 = pd.read_csv('../data/tables/' + self.article_identifier +'_tables_table_4.csv', header=None)
        if self.p['Atmosphere'] == 0:
            exponent = table_4.iloc[1, 1]
        elif self.p['Atmosphere'] == 1:
            exponent = table_4.iloc[1, 2]
        elif self.p['Atmosphere'] == 2:
            exponent = table_4.iloc[1, 3]
        else:
            exponent = (0.570 + 
            0.0057 * self.p['Chloride pollution annual average'] * self.p['Temperature'] + 
            7.7e-4 * self.p['Wetness time']*365 - 
            1.7e-3 * self.eval_annual_corrosion())

        return float(exponent)
    

    def eval_material_loss(self, time):

        material_loss = self.eval_annual_corrosion()*np.power(time, self.evaluate_exponent())
        return material_loss
    

def load_data(model_identifier):
    table_2 = pd.read_csv('../data/tables/' + model_identifier +'_tables_table_2.csv', header=None)
    table_4 = pd.read_csv('../data/tables/' + model_identifier +'_tables_table_4.csv', header=None)

    return table_2, table_4


def get_atmosphere_types(table_4):
    atmosphere_types = table_4.iloc[0, 1:]
    atmosphere_types['4'] = "Enter Cl^- and SO_2 pollution annual averages"

    return atmosphere_types.to_list()


def get_parameters(table_2, atmosphere, atmosphere_types):
    parameters = {}
    parameters['Binary Interaction'] = st.selectbox('Use Binary Interaction?', ((True, False,)))
    parameters['Atmosphere'] = atmosphere_types.index(atmosphere)
    parameters['Chloride pollution annual average'] = float(table_2.iloc[7, 2])
    parameters['SO2 pollution annual average'] = float(table_2.iloc[7, 2])
    if parameters['Atmosphere'] == 3:
        parameters['Chloride pollution annual average'] = float(st.text_input(r"$Cl^-$ - Chloride pollution annual average  $[mg Cl^{-} dm^{-2} d^{-1}]$,", str(table_2.iloc[7, 2])))
        parameters['SO2 pollution annual average'] = float(st.text_input(r"$SO_2$ - SO2 pollution annual average  $[mg SO_2 dm^{-2} d^{-1}]$,", str(table_2.iloc[7, 2])))
    parameters['Temperature'] = float(st.text_input(r"$T$ - Temperature [°C]", str(table_2.iloc[6, 2])))
    parameters['Wetness time'] = float(st.text_input(r"$T_w$ - Wetness time [annual fraction]", str(table_2.iloc[4, 2])))

    return parameters


def display_formulas(parameters):
    if parameters['Binary Interaction']:
        st.write(r'Annual corrosion, $A [um]$ = $132.4Cl^-(1 + 0.038T - 1.96t_w - 0.53SO_2 + 74.6t_w(1 + 1.07SO_2) - 6.3)$ ')
    else:
        st.write(r'Annual corrosion, $A [um]$ = $33.0 + 57.4Cl^- + 26.6SO_2$')
    st.write(r'Exponent, $n = 0.570 + 0.0057Cl^-T + 7.7 \times 10^{-4}D - 1.7 \times 10^{-3}A$')


def AC_model_fileu1993(model_identifier):
    time = st.number_input('Enter duration [years]:', min_value=1.0, max_value=100.0, step=0.1) 
    table_2, table_4 = load_data(model_identifier)
    atmosphere_types = get_atmosphere_types(table_4)
    atmosphere = st.selectbox('Select Atmosphere:', ((atmosphere_types)))
    parameters = get_parameters(table_2, atmosphere, atmosphere_types)
    display_formulas(parameters)

    return i_the_prediction_of_atmospheric_corrosion_from_met(parameters), time
