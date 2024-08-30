import pandas as pd
import streamlit as st
import numpy as np
from .corrosion_model import CorrosionModel

class iso_9224(CorrosionModel):

    def __init__(self, parameters, article_identifier):
        CorrosionModel.__init__(self)
        self.model_name = 'ISO 9223:2012 and ISO 9224:2012'
        self.article_identifier = article_identifier
        self.steel = "Unalloyed Steel"
        self.p = parameters
        self.correlation_speed_provided = 'corrosion_speed' in parameters

    
    def eval_corrosion_speed(self):

        if self.p['T'] <= 10:
            fst = 0.15*(self.p['T'] - 10)
        else:
            fst = -0.054*(self.p['T'] - 10)

        corrosion_speed = 1.77*self.p['Pd']**0.52*np.e**(0.02*self.p['RH'] + fst) + 0.102*self.p['Sd']**0.62*np.e**(0.033*self.p['RH'] + 0.04*self.p['T'])
        return corrosion_speed


    def eval_material_loss(self, time):
        
        if self.correlation_speed_provided:
            corrosion_speed = self.p['corrosion_speed']
        else:
            corrosion_speed = self.eval_corrosion_speed()
        
        if np.max(time) < 20:
            material_loss = self.p['exponent']*corrosion_speed*time**(self.p['exponent'] - 1)
        else:
            material_loss = corrosion_speed*(20**self.p['exponent'] + self.p['exponent']*20**(self.p['exponent'] - 1)*(time - 20))

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
    table_2 = pd.read_csv('../data/tables/' + article_identifier +'_tables_table_2.csv', header=None)
    table_3 = pd.read_csv('../data/tables/' + article_identifier +'_tables_table_3.csv', header=None)
    table_b3 = pd.read_csv('../data/tables/' + article_identifier +'_tables_table_B.3.csv', header=None)
    table_b4 = pd.read_csv('../data/tables/' + article_identifier +'_tables_table_B.4.csv', header=None)
    table_c1 = pd.read_csv('../data/tables/' + article_identifier +'_tables_table_C.1.csv', header=None)
    table_9224_3 = pd.read_csv('../data/tables/' + article_identifier +'_tables_9224_table_3.csv', header=None)

    return table_2, table_3, table_b3, table_b4, table_c1, table_9224_3


def get_corrosion_type(table_c1):
    table_c1_disp_values = table_c1.iloc[1:, 1]
    table_c1_disp_values['7'] = "Manually enter Cl^- and SO_2 annual deposits, relative humudity and temperature"

    return table_c1_disp_values.tolist()


def get_corrosion_speed(corrosion_type, table_2):
    st.table(table_2)
    corrosion_speed_type = ['Use lower limit', 'Use upper limit', 'Use average']
    corrosion_speed = st.selectbox('Select corrosion speed?', ((corrosion_speed_type)))
    corrosion_speed = corrosion_speed_type.index(corrosion_speed)

    if corrosion_speed == 0:
        corrosion_speed = float(table_2.iloc[corrosion_type+1, 2])
    elif corrosion_speed == 1:
        corrosion_speed = float(table_2.iloc[corrosion_type+1, 3])
    else:
        corrosion_speed = (float(table_2.iloc[corrosion_type+1, 2]) + float(table_2.iloc[corrosion_type+1, 3]))/2

    st.write('Corrosion speed = ' + str(corrosion_speed))

    return corrosion_speed


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


def get_exponent(time, table_9224_3):
    exponent_types = ['Use DIN recommeneded time exponents measured from the ISO CORRAG program', 'Enter manually']     
    exponent_type = st.selectbox('Please select the time exponent', ((exponent_types)))
    exponent_type = exponent_types.index(exponent_type)
    if exponent_type == 0:
        # Get the exponent value
        exponent = get_exponent_value(time, table_9224_3.iloc[6:, :2])
        # Display the result
        st.write(f"The exponent value for year {time:.2f} is {exponent:.2f}")
    else:
        exponent = st.number_input('Enter exponent:')

    return exponent


def AC_model_iso9223(article_identifier):
    time = st.number_input('Enter duration [years]:', min_value=1.0, max_value=100.0, step=0.1) 
    table_2, table_3, table_b3, table_b4, table_c1, table_9224_3 = load_data(article_identifier)
    st.table(table_c1)
    corrosion_type = st.selectbox('Select corrosion type?', ((get_corrosion_type(table_c1))))
    corrosion_type = get_corrosion_type(table_c1).index(corrosion_type)
    parameters = {}
    if corrosion_type < 6:
        parameters['corrosion_speed'] = get_corrosion_speed(corrosion_type, table_2)
    else:
        st.table(table_3)
        st.write('### Parameters used in deriving the dose-response functions, including symbol, description, interval and unit')
        st.table(table_b3)
        st.write(r'### Classification of contamination by sulfur-containing substances, represented by $SO_2$')
        st.table(table_b4)
        st.write(r'### Classification of contamination by sulfur-containing substances, represented by $Cl^-$')

        limits = {
        'T': {'desc': 'Temperature', 'lower': -17.1, 'upper': 28.7, 'unit': '°C'},
        'RH': {'desc': 'Relative Humidity', 'lower': 34, 'upper': 93, 'unit': '%'},
        'Pd': {'desc': 'SO₂-Deposit', 'lower': 0.7, 'upper': 150.4, 'unit': 'mg/(m²⋅d)'},
        'Sd': {'desc': 'Cl⁻-Deposit', 'lower': 0.4, 'upper': 760.5, 'unit': 'mg/(m²⋅d)'}
        }
        for symbol in limits.keys():
            parameters[symbol] = get_input(symbol, limits)
    parameters['exponent'] = get_exponent(time, table_9224_3)
    
    return iso_9224(parameters, article_identifier), time
