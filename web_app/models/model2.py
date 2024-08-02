import pandas as pd
import streamlit as st
import numpy as np
from . atmospheric_corrosion_models import iso_9224


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


def model2(model_identifier):

    table_2 = pd.read_csv('../data/tables/' + model_identifier +'_tables_table_2.csv', header=None)
    table_3 = pd.read_csv('../data/tables/' + model_identifier +'_tables_table_3.csv', header=None)
    table_b3 = pd.read_csv('../data/tables/' + model_identifier +'_tables_table_B.3.csv', header=None)
    table_b4 = pd.read_csv('../data/tables/' + model_identifier +'_tables_table_B.4.csv', header=None)
    table_c1 = pd.read_csv('../data/tables/' + model_identifier +'_tables_table_C.1.csv', header=None)
    table_9224_3 = pd.read_csv('../data/tables/' + model_identifier +'_tables_9224_table_3.csv', header=None)

    # Streamlit input for the year
    time = st.number_input('Enter duration [years]:', min_value=1.0, max_value=100.0, step=0.1) 

    st.table(table_c1)
    table_c1_disp_values = table_c1.iloc[1:, 1]
    table_c1_disp_values['7'] = "Manually enter Cl^- and SO_2 annual deposits, relative humudity and temperature"
    table_c1_disp_values = table_c1_disp_values.tolist()
    corrosion_type = st.selectbox(
    'Select corrosion type?',
    ((table_c1_disp_values))
    )
    corrosion_type = table_c1_disp_values.index(corrosion_type)

    corrosion_speed_type = ['Use lower limit', 'Use upper limit', 'Use average']

    parameters = {}
    if corrosion_type < 6:
        st.table(table_2)
        corrosion_speed = st.selectbox(
        'Select corrosion speed?',
        ((corrosion_speed_type))
        )
        corrosion_speed = corrosion_speed_type.index(corrosion_speed)

        if corrosion_speed == 0:
            corrosion_speed = float(table_2.iloc[corrosion_type+1, 2])
        elif corrosion_speed == 1:
            corrosion_speed = float(table_2.iloc[corrosion_type+1, 3])
        else:
            corrosion_speed = (float(table_2.iloc[corrosion_type+1, 2]) + float(table_2.iloc[corrosion_type+1, 3]))/2

        st.write('Corrosion speed = ' + str(corrosion_speed))

        parameters['Corrosion_speed'] = float(corrosion_speed)

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
        
        def get_input(symbol):
            limit = limits[symbol]
            value = st.text_input(f"Enter {limit['desc']} ({symbol}) [{limit['unit']}]:", value='')
            
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

        for symbol in limits.keys():
            parameters[symbol] = get_input(symbol)

    exponent_types = ['Use DIN recommeneded time exponents measured from the ISO CORRAG program', 'Enter manually']     
    exponent_type = st.selectbox(
    'Please select the time exponent',
    ((exponent_types))
    )
    exponent_type = exponent_types.index(exponent_type)
    if exponent_type == 0:
        # Get the exponent value
        exponent = get_exponent_value(time, table_9224_3.iloc[6:, :2])

        # Display the result
        st.write(f"The exponent value for year {time:.2f} is {exponent:.2f}")

    else:
        exponent = st.number_input('Enter exponent:')

    parameters['exponent'] = exponent

    return iso_9224(parameters)