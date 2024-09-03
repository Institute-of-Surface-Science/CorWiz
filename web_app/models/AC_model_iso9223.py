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

    DATA_FILE_PATHS = {
        'table_2': '../data/tables/din-en-iso-92232012-05_tables_table_2.csv',
        'table_3': '../data/tables/din-en-iso-92232012-05_tables_table_3.csv',
        'table_b3': '../data/tables/din-en-iso-92232012-05_tables_table_B.3.csv',
        'table_b4': '../data/tables/din-en-iso-92232012-05_tables_table_B.4.csv',
        'table_c1': '../data/tables/din-en-iso-92232012-05_tables_table_C.1.csv',
        'table_9224_3': '../data/tables/din-en-iso-92232012-05_tables_9224_table_3.csv'
    }

    def __init__(self, parameters: Optional[dict] = None):
        super().__init__(model_name='ISO 9223:2012 and ISO 9224:2012')
        self.parameters = parameters if parameters else {}
        self.table_2, self.table_3, self.table_b3, self.table_b4, self.table_c1, self.table_9224_3 = self._load_data()
        self._initialize_model()

    def _load_data(self) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Loads the relevant data tables for the ISO 9224 model."""
        return (
            pd.read_csv(self.DATA_FILE_PATHS['table_2'], header=None),
            pd.read_csv(self.DATA_FILE_PATHS['table_3'], header=None),
            pd.read_csv(self.DATA_FILE_PATHS['table_b3'], header=None),
            pd.read_csv(self.DATA_FILE_PATHS['table_b4'], header=None),
            pd.read_csv(self.DATA_FILE_PATHS['table_c1'], header=None),
            pd.read_csv(self.DATA_FILE_PATHS['table_9224_3'], header=None)
        )

    def _initialize_model(self) -> None:
        """Initializes the model by setting up the parameters and selecting corrosion type."""
        with st.expander("Description Corrosion Type"):
            st.table(self.table_c1)

        corrosion_types = self.table_c1.iloc[1:, 1].tolist()
        corrosion_types.append("Manually enter Cl^- and SO_2 annual deposits, relative humidity, and temperature")

        corrosion_type = st.selectbox('Select corrosion type:', corrosion_types)
        corrosion_type_index = corrosion_types.index(corrosion_type)

        if corrosion_type_index < 6:
            self._handle_predefined_corrosion_type(corrosion_type_index)
        else:
            self._handle_custom_corrosion_type()

        self.parameters['exponent'] = self._determine_exponent()

    def _handle_predefined_corrosion_type(self, corrosion_type_index: int) -> None:
        """Handles predefined corrosion types by setting the corrosion speed."""
        corrosion_speed_options = ['Use lower limit', 'Use upper limit', 'Use average']
        selected_option = st.selectbox('Select corrosion speed option:', corrosion_speed_options)

        if selected_option == 'Use lower limit':
            self.parameters['corrosion_speed'] = float(self.table_2.iloc[corrosion_type_index + 1, 2])
        elif selected_option == 'Use upper limit':
            self.parameters['corrosion_speed'] = float(self.table_2.iloc[corrosion_type_index + 1, 3])
        else:  # 'Use average'
            lower_limit = float(self.table_2.iloc[corrosion_type_index + 1, 2])
            upper_limit = float(self.table_2.iloc[corrosion_type_index + 1, 3])
            self.parameters['corrosion_speed'] = (lower_limit + upper_limit) / 2

        st.write(f'Corrosion speed selected: {self.parameters["corrosion_speed"]:.2f} μm/year')

    def _handle_custom_corrosion_type(self) -> None:
        """Handles custom corrosion types by prompting the user for detailed environmental inputs."""
        with st.expander("Typical Values:"):
            st.table(self.table_3)
            st.write(
                '### Parameters used in deriving the dose-response functions, including symbol, description, interval, and unit')
            st.table(self.table_b3)
            st.write(r'### Classification of contamination by sulfur-containing substances, represented by $SO_2$')
            st.table(self.table_b4)
            st.write(r'### Classification of contamination by sulfur-containing substances, represented by $Cl^-$')

        limits = {
            'T': {'desc': 'Temperature', 'lower': -17.1, 'upper': 28.7, 'unit': '°C'},
            'RH': {'desc': 'Relative Humidity', 'lower': 34, 'upper': 93, 'unit': '%'},
            'Pd': {'desc': 'SO₂-Deposit', 'lower': 0.7, 'upper': 150.4, 'unit': 'mg/(m²⋅d)'},
            'Sd': {'desc': 'Cl⁻-Deposit', 'lower': 0.4, 'upper': 760.5, 'unit': 'mg/(m²⋅d)'}
        }
        for symbol, limit in limits.items():
            value = st.text_input(f"Enter {limit['desc']} ({symbol}) [{limit['unit']}]:", value=limit['lower'])
            self.parameters[symbol] = float(value)

    def _determine_exponent(self) -> float:
        """Determines or interpolates the exponent to be used in the material loss calculation."""
        exponent_types = ['Use DIN recommended time exponents measured from the ISO CORRAG program', 'Enter manually']
        exponent_type = st.selectbox('Please select the time exponent', exponent_types)

        if exponent_type == exponent_types[0]:
            time = st.number_input('Enter duration [years]:', min_value=1.0, max_value=100.0, step=0.1,
                                   key="duration_years")
            years = np.array(self.table_9224_3.iloc[6:, 0].astype(int))
            exponents = np.array(self.table_9224_3.iloc[6:, 1].astype(float))

            if time in years:
                return float(exponents[years == time][0])
            else:
                return float(np.interp(time, years, exponents))
        else:
            return float(st.number_input('Enter exponent:', key="manual_exponent"))

    def eval_material_loss(self, time: float) -> float:
        """Calculates and returns the material loss over time based on the provided parameters."""

        # Calculate corrosion speed if not provided
        if 'corrosion_speed' in self.parameters:
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


# Example of usage
def run_iso9223_model() -> Tuple[ISO9224Model, float]:
    """
    Runs the ISO 9224 corrosion model.

    Returns:
        Tuple[ISO9224Model, float]: An instance of the ISO9224Model class and the duration for which the model is evaluated.
    """
    model = ISO9224Model()
    time_duration = st.number_input('Enter duration [years]:', min_value=1.0, max_value=100.0, step=0.1)
    return model, time_duration
