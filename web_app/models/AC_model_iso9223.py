import pandas as pd
import streamlit as st
import numpy as np
from typing import Tuple, Optional
from .corrosion_model import CorrosionModel


class ISO9224Model(CorrosionModel):
    """
    A corrosion model based on ISO 9223:2012 and ISO 9224:2012 standards.

    This model predicts material loss due to atmospheric corrosion based on various environmental factors.
    """

    def __init__(self, parameters: dict):
        super().__init__(model_name='ISO 9223:2012 and ISO 9224:2012')
        self.steel = "Unalloyed Steel"
        self.parameters = parameters
        self.article_identifier = "din-en-iso-92232012-05"
        self.correlation_speed_provided = 'corrosion_speed' in parameters
        self.table_2, self.table_3, self.table_b3, self.table_b4, self.table_c1, self.table_9224_3 = self._load_data()

    def _load_data(self) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Loads the relevant data tables for the ISO 9224 model."""
        table_2 = pd.read_csv(f'../data/tables/{self.article_identifier}_tables_table_2.csv', header=None)
        table_3 = pd.read_csv(f'../data/tables/{self.article_identifier}_tables_table_3.csv', header=None)
        table_b3 = pd.read_csv(f'../data/tables/{self.article_identifier}_tables_table_B.3.csv', header=None)
        table_b4 = pd.read_csv(f'../data/tables/{self.article_identifier}_tables_table_B.4.csv', header=None)
        table_c1 = pd.read_csv(f'../data/tables/{self.article_identifier}_tables_table_C.1.csv', header=None)
        table_9224_3 = pd.read_csv(f'../data/tables/{self.article_identifier}_tables_9224_table_3.csv', header=None)
        return table_2, table_3, table_b3, table_b4, table_c1, table_9224_3

    def eval_material_loss(self, time: float) -> float:
        """Calculates and returns the material loss over time based on the provided parameters."""

        # Calculate corrosion speed if not provided
        if self.correlation_speed_provided:
            corrosion_speed = self.parameters['corrosion_speed']
        else:
            if self.parameters['T'] <= 10:
                fst = 0.15 * (self.parameters['T'] - 10)
            else:
                fst = -0.054 * (self.parameters['T'] - 10)

            corrosion_speed = (1.77 * self.parameters['Pd'] ** 0.52 * np.exp(0.02 * self.parameters['RH'] + fst) +
                               0.102 * self.parameters['Sd'] ** 0.62 * np.exp(
                        0.033 * self.parameters['RH'] + 0.04 * self.parameters['T']))

        # Calculate material loss over time
        if np.max(time) < 20:
            material_loss = self.parameters['exponent'] * corrosion_speed * time ** (self.parameters['exponent'] - 1)
        else:
            material_loss = corrosion_speed * (20 ** self.parameters['exponent'] +
                                               self.parameters['exponent'] * 20 ** (self.parameters['exponent'] - 1) * (
                                                           time - 20))

        return material_loss

def get_corrosion_type(table_c1: pd.DataFrame) -> list:
    """
    Returns a list of corrosion types from the provided table.

    Args:
        table_c1 (pd.DataFrame): The dataframe containing corrosion type information.

    Returns:
        list: A list of corrosion types.
    """
    table_c1_disp_values = table_c1.iloc[1:, 1].tolist()
    table_c1_disp_values.append("Manually enter Cl^- and SO_2 annual deposits, relative humidity, and temperature")
    return table_c1_disp_values


def get_input(symbol: str, limits: dict) -> float:
    """
    Prompts the user to input a value for a specific parameter within defined limits.

    Args:
        symbol (str): The symbol for the parameter (e.g., 'T' for temperature).
        limits (dict): A dictionary containing descriptions, lower and upper limits, and units for the parameter.

    Returns:
        float: The user-inputted value, validated within the defined limits.
    """
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


def get_exponent(time: float, table_9224_3: pd.DataFrame) -> float:
    """
    Determines the exponent to be used in the material loss calculation.

    Args:
        time (float): The duration for which the model is evaluated.
        table_9224_3 (pd.DataFrame): The dataframe containing exponent data.

    Returns:
        float: The calculated or manually entered exponent.
    """
    exponent_types = ['Use DIN recommended time exponents measured from the ISO CORRAG program', 'Enter manually']
    exponent_type = st.selectbox('Please select the time exponent', exponent_types)

    if exponent_type == exponent_types[0]:
        exponent = get_exponent_value(time, table_9224_3.iloc[6:, :2])
        st.write(f"The exponent value for year {time:.2f} is {exponent:.2f}")
    else:
        exponent = st.number_input('Enter exponent:')

    return exponent


def get_exponent_value(year: float, table: pd.DataFrame) -> float:
    """
    Interpolates the exponent value for a given year from a table.

    Args:
        year (float): The year for which to calculate the exponent.
        table (pd.DataFrame): The table containing year and exponent data.

    Returns:
        float: The interpolated or exact exponent value.
    """
    years = np.array(table[0].astype(int))
    exponents = np.array(table[1].astype(float))

    if year in years:
        return exponents[years == year][0]
    else:
        return np.interp(year, years, exponents)

def get_corrosion_speed(corrosion_type_index: int, table_2: pd.DataFrame) -> float:
    """
    Determines the corrosion speed based on the selected corrosion type.

    Args:
        corrosion_type_index (int): The index of the selected corrosion type.
        table_2 (pd.DataFrame): The dataframe containing corrosion speed data.

    Returns:
        float: The calculated corrosion speed.
    """
    corrosion_speed_options = ['Use lower limit', 'Use upper limit', 'Use average']
    selected_option = st.selectbox('Select corrosion speed option:', corrosion_speed_options)

    if selected_option == 'Use lower limit':
        corrosion_speed = float(table_2.iloc[corrosion_type_index + 1, 2])
    elif selected_option == 'Use upper limit':
        corrosion_speed = float(table_2.iloc[corrosion_type_index + 1, 3])
    else:  # 'Use average'
        lower_limit = float(table_2.iloc[corrosion_type_index + 1, 2])
        upper_limit = float(table_2.iloc[corrosion_type_index + 1, 3])
        corrosion_speed = (lower_limit + upper_limit) / 2

    st.write(f'Corrosion speed selected: {corrosion_speed:.2f} μm/year')
    return corrosion_speed


def AC_model_iso9223(article_identifier: str) -> Tuple[ISO9224Model, float]:
    """
    Executes the ISO 9224 corrosion model.

    Returns:
        Tuple[ISO9224Model, float]: An instance of the ISO9224Model class and the duration for which the model is evaluated.
    """
    time = st.number_input('Enter duration [years]:', min_value=1.0, max_value=100.0, step=0.1)
    table_2, table_3, table_b3, table_b4, table_c1, table_9224_3 = ISO9224Model(parameters={})._load_data()

    with st.expander("Description Corrosion Type"):
        st.table(table_c1)
    corrosion_type = st.selectbox('Select corrosion type:', get_corrosion_type(table_c1))
    corrosion_type_index = get_corrosion_type(table_c1).index(corrosion_type)

    parameters = {}
    if corrosion_type_index < 6:
        parameters['corrosion_speed'] = get_corrosion_speed(corrosion_type_index, table_2)
    else:
        st.table(table_3)
        st.write(
            '### Parameters used in deriving the dose-response functions, including symbol, description, interval, and unit')
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

    model = ISO9224Model(parameters=parameters)

    return model, time
