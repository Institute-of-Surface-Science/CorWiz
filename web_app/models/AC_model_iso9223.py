import pandas as pd
import streamlit as st
import numpy as np
from typing import Dict, Tuple, Optional
from scipy.interpolate import interp1d
from .corrosion_model import CorrosionModel

class ISO9223Model(CorrosionModel):
    """
    A corrosion model based on ISO 9223:2012 and ISO 9224:2012 standards.

    This model predicts material loss due to atmospheric corrosion based on various environmental factors.
    """

    DATA_FILE_PATHS = {
        'table_2': '../data/tables/din-en-iso-92232012-05_tables_table_2.csv',
        'table_3': '../data/tables/din-en-iso-92232012-05_tables_table_3.csv',
        'table_b3': '../data/tables/din-en-iso-92232012-05_tables_table_B.3.csv',
        'table_b4': '../data/tables/din-en-iso-92232012-05_tables_table_B.4.csv',
        'table_c1': '../data/tables/din-en-iso-92232012-05_tables_table_C.1.csv',
        'table_9224_3': '../data/tables/din-en-iso-92232012-05_tables_9224_table_3.csv'
    }

    def __init__(self, json_file_path: str):
        super().__init__(json_file_path=json_file_path, model_name='ISO9223Model')
        self.parameters: Dict[str, float] = {}
        self.table_2, self.table_3, self.table_b3, self.table_b4, self.table_c1, self.table_9224_3 = self._load_data()

    def _load_data(self) -> Tuple[pd.DataFrame, ...]:
        """Loads and returns all relevant data tables for the ISO 9224 model."""
        return tuple(pd.read_csv(self.DATA_FILE_PATHS[key], header=None) for key in self.DATA_FILE_PATHS)

    def display_parameters(self) -> None:
        """Displays the parameter selection interface for the user."""
        with st.expander("Description Corrosion Type"):
            st.table(self.table_c1)

        corrosion_types = self.table_c1.iloc[1:, 1].tolist()
        corrosion_types.append("Manually enter Cl⁻ and SO₂ annual deposits, relative humidity, and temperature")

        corrosion_type = st.selectbox('Select corrosion type:', corrosion_types)
        corrosion_type_index = corrosion_types.index(corrosion_type)

        if corrosion_type_index < 6:
            corrosion_speed_options = ['Use lower limit', 'Use upper limit', 'Use average']
            selected_option = st.selectbox('Select corrosion speed option:', corrosion_speed_options)

            lower_limit = float(self.table_2.iloc[corrosion_type_index + 1, 2])
            upper_limit = float(self.table_2.iloc[corrosion_type_index + 1, 3])

            if selected_option == 'Use lower limit':
                self.parameters['corrosion_speed'] = lower_limit
            elif selected_option == 'Use upper limit':
                self.parameters['corrosion_speed'] = upper_limit
            else:
                self.parameters['corrosion_speed'] = (lower_limit + upper_limit) / 2

            st.write(f"Corrosion speed selected: {self.parameters['corrosion_speed']:.2f} μm/year")
        else:
            with st.expander("Typical Values:"):
                st.table(self.table_3)
                st.write("### Parameters used in deriving the dose-response functions")
                st.table(self.table_b3)
                st.write("### Classification of contamination by sulfur-containing substances, represented by SO₂ and Cl⁻")
                st.table(self.table_b4)

            limits = {
                'T': {'desc': 'Temperature', 'lower': -17.1, 'upper': 28.7, 'unit': '°C'},
                'RH': {'desc': 'Relative Humidity', 'lower': 34, 'upper': 93, 'unit': '%'},
                'Pd': {'desc': 'SO₂-Deposit', 'lower': 0.7, 'upper': 150.4, 'unit': 'mg/(m²⋅d)'},
                'Sd': {'desc': 'Cl⁻-Deposit', 'lower': 0.4, 'upper': 760.5, 'unit': 'mg/(m²⋅d)'}
            }

            for symbol, limit in limits.items():
                value = st.number_input(f"Enter {limit['desc']} ({symbol}) [{limit['unit']}]:",
                                        value=limit['lower'], min_value=limit['lower'], max_value=limit['upper'])
                self.parameters[symbol] = float(value)

    def _determine_exponent(self, time: float) -> float:
        """Determines or interpolates the time exponent for the material loss calculation."""
        exponent_types = ['Use DIN recommended time exponents measured from the ISO CORRAG program', 'Enter manually']
        selected_type = st.selectbox('Please select the time exponent', exponent_types)

        years = self.table_9224_3.iloc[6:, 0].astype(int).values  # 'table_9224_3'
        exponents = self.table_9224_3.iloc[6:, 1].astype(float).values

        if selected_type == exponent_types[0]:
            max_time = np.max(time) if isinstance(time, np.ndarray) else time

            if max_time in years:
                return float(exponents[years == max_time][0])
            else:
                return float(np.interp(max_time, years, exponents))
        else:
            return float(st.number_input('Enter exponent:', key="manual_exponent"))

    def evaluate_material_loss(self, time: float) -> float:
        """Calculates and returns the material loss over time based on the provided parameters."""
        self.parameters['exponent'] = self._determine_exponent(time)

        if 'corrosion_speed' in self.parameters:
            corrosion_speed = self.grams_to_um_map(self.parameters['corrosion_speed'])
            material_loss = time*corrosion_speed
        else:
            if self.parameters['T'] <= 10:
                temperature_factor = 0.15 * (self.parameters['T'] - 10)
            else:
                temperature_factor = -0.054 * (self.parameters['T'] - 10)

            corrosion_speed = (
                1.77 * self.parameters['Pd'] ** 0.52 * np.exp(0.02 * self.parameters['RH'] + temperature_factor) +
                0.102 * self.parameters['Sd'] ** 0.62 * np.exp(0.033 * self.parameters['RH'] + 0.04 * self.parameters['T'])
            )

        return self.parameters['exponent'] * corrosion_speed * time ** (self.parameters['exponent'] - 1)

    def grams_to_um_map(self, corrosion_speed: float) -> float:
        """Maps corrosion speed from g/(m²⋅a) to μm/a."""
        g_to_um_mapping = interp1d([10, 200, 400, 650, 1500, 500], [1.3, 25, 50, 80, 200, 700], kind='linear', fill_value='extrapolate')
        return g_to_um_mapping(corrosion_speed)

    def um_to_grams_map(self, corrosion_speed: float) -> float:
        """Maps corrosion speed from μm/a to g/(m²⋅a)."""
        um_to_g_mapping = interp1d([1.3, 25, 50, 80, 200, 700], [10, 200, 400, 650, 1500, 500], kind='linear', fill_value='extrapolate')
        return um_to_g_mapping(corrosion_speed)

