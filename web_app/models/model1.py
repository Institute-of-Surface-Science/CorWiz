import pandas as pd
import streamlit as st
from . atmospheric_corrosion_models import i_the_prediction_of_atmospheric_corrosion_from_met


def model1(model_identifier):


    time = st.number_input('Enter duration [years]:', min_value=1.0, max_value=100.0, step=0.1) 

    table_2 = pd.read_csv('../data/tables/' + model_identifier +'_tables_table_2.csv', header=None)
    table_4 = pd.read_csv('../data/tables/' + model_identifier +'_tables_table_4.csv', header=None)
    atmosphere_types = table_4.iloc[0, 1:]
    atmosphere_types['4'] = "Enter Cl^- and SO_2 pollution annual averages"
    atmosphere_types = atmosphere_types.to_list()
    binary_interaction = st.selectbox(
    'Use Binary Interaction?',
    ((True, False,))
    )

    atmosphere = st.selectbox(
    'Select atmosphere:',
    ((atmosphere_types))
    )
    
    Cl = float(table_2.iloc[7, 2])
    SO2 = float(table_2.iloc[7, 2])
    atmosphere = atmosphere_types.index(atmosphere)
    if atmosphere == 3:
        Cl = float(st.text_input(r"$Cl^-$ - chloride pollution annual average  $[mg Cl^{-} dm^{-2} d^{-1}]$,", str(table_2.iloc[7, 2])))
        SO2 = float(st.text_input(r"$SO_2$ - SO2 pollution annual average  $[mg SO_2 dm^{-2} d^{-1}]$,", str(table_2.iloc[7, 2])))
    temp = float(st.text_input(r"$T$ - Temperature [°C]", str(table_2.iloc[6, 2])))
    tw = float(st.text_input(r"$T_w$ - Wetness time [annual fraction]", str(table_2.iloc[4, 2])))
    D = float(st.text_input(r"$D$ - Number of rainy days per year [days]", str(table_2.iloc[5, 2])))

    if binary_interaction:
        st.write(r'Annual corrosion, A $[um]$ = $132.4Cl^-(1 + 0.038T - 1.96t_w - 0.53SO_2 + 74.6t_w(1 + 1.07SO_2) - 6.3)$ ')
    else:
        st.write(r'Annual corrosion, A $[um]$ = $33.0 + 57.4Cl^- + 26.6SO_2$')

    st.write(r'Exponent, n = $0.570 + 0.0057Cl^-T + 7.7 \times 10^{-4}D - 1.7 \times 10^{-3}A$')

    parameters = {
    'Cl': Cl,    # Chloride concentration
    'SO2': SO2,  # Sulfur dioxide concentration
    'temp': temp,  # Temperature
    'tw': tw,    # Time
    'D': D       # Material parameter or other variable
    }
    
    return i_the_prediction_of_atmospheric_corrosion_from_met(binary_interaction, atmosphere, parameters), time