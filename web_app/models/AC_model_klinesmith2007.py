import streamlit as st
import pandas as pd
import numpy as np
from typing import Dict, Optional
from .corrosion_model import CorrosionModel

class KlineSmith2007Model(CorrosionModel):
    """
    A corrosion model based on the study by Klinesmith et al. (2007) which evaluates the effect of environmental
    conditions on corrosion rates.

    Reference:
        Klinesmith, Dawn E., McCuen, Richard H., and Albrecht, Pedro.
        "Effect of environmental conditions on corrosion rates."
        Journal of Materials in Civil Engineering, 19(2), 121-129 (2007). ASCE.
    """

    DATA_FILE_PATH = '../data/tables/klinesmith2007_tables_table_2.csv'

    def __init__(self):
        super().__init__(model_name='Effect of Environmental Conditions on Corrosion Rates')
        self.specimen_type = self._select_specimen_type()
        self.coefficients = self._load_coefficients()
        self.parameters = {}

    def _select_specimen_type(self) -> str:
        """Allows the user to select the specimen type dynamically from the CSV file."""
        table_2 = pd.read_csv(self.DATA_FILE_PATH)
        specimen_types = table_2['Specimen'].str.strip().unique()  # Extract and clean up specimen types
        return st.selectbox('Select specimen type:', specimen_types)

    def _load_coefficients(self) -> Dict[str, float]:
        """Loads coefficients dynamically from the CSV file based on the selected specimen type."""
        table_2 = pd.read_csv(self.DATA_FILE_PATH)

        # Select the row corresponding to the selected specimen type
        row = table_2.loc[table_2['Specimen'].str.strip() == self.specimen_type].iloc[0]

        # Automatically map all relevant columns to coefficients
        coefficients = {col: float(row[col]) for col in table_2.columns[2:]}

        return coefficients

    def display_parameters(self) -> None:
        """Prompts the user to input values for all parameters within defined limits."""
        limits = {
            'T': {'desc': 'Temperature', 'lower': -17.1, 'upper': 28.7, 'unit': '°C'},
            'TOW': {'desc': 'Time of Wetness', 'lower': 0.01, 'upper': 1.0, 'unit': 'annual fraction'},
            'SO2': {'desc': 'SO₂ Deposit', 'lower': 0.7, 'upper': 150.4, 'unit': 'mg/(m²⋅d)'},
            'Cl': {'desc': 'Cl⁻ Deposit', 'lower': 0.4, 'upper': 760.5, 'unit': 'mg/(m²⋅d)'}
        }

        for symbol, limit in limits.items():
            self.parameters[symbol] = st.number_input(
                f"Enter {limit['desc']} ({symbol}) [{limit['unit']}]:",
                min_value=limit['lower'],
                max_value=limit['upper'],
                value=limit['lower'],
                step=0.01,
                key=f"input_{symbol}"
            )

    def evaluate_material_loss(self, time: float) -> float:
        """Calculates the material loss over time based on the provided environmental parameters."""
        coeffs = self.coefficients

        # Calculate material loss using the model equation
        material_loss = (
            coeffs['A'] * (time ** coeffs['B']) *
            ((self.parameters['TOW'] * 365 * 24 / coeffs['C']) ** coeffs['D']) *
            (1 + (self.parameters['SO2'] / coeffs['E']) ** coeffs['F']) *
            (1 + (self.parameters['Cl'] / coeffs['G']) ** coeffs['H']) *
            (np.exp(coeffs['J'] * (self.parameters['T'] + coeffs['T0'])))
        )

        return material_loss
