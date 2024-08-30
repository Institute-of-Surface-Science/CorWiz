import streamlit as st
import pandas as pd
import numpy as np
from typing import Dict, Tuple
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

    def __init__(self, parameters: Dict[str, float]):
        super().__init__(model_name='Effect of Environmental Conditions on Corrosion Rates')
        self.steel = "Carbon Steel"
        self.parameters = parameters
        self.article_identifier = "klinesmith2007"

    def eval_material_loss(self, time: float) -> float:
        """Calculates the material loss over time based on the provided environmental parameters."""

        # Load data from the relevant table
        table_2 = pd.read_csv(f'../data/tables/{self.article_identifier}_tables_table_2.csv', header=None)

        # Extract coefficients from the table
        A, B, C, D, E, F, G, H, J, T0 = [float(table_2.iloc[1, i]) for i in range(2, 12)]

        # Calculate material loss using the model equation
        material_loss = (
            A * (time ** B) *
            ((self.parameters['TOW'] * 365 * 24 / C) ** D) *
            (1 + (self.parameters['SO2'] / E) ** F) *
            (1 + (self.parameters['Cl'] / G) ** H) *
            (np.exp(J * (self.parameters['T'] + T0)))
        )

        return material_loss


def get_parameters(limits: Dict[str, Dict[str, float]]) -> Dict[str, float]:
    """
    Prompts the user to input values for all parameters within defined limits and returns a dictionary of the parameters.

    Args:
        limits (Dict[str, Dict[str, float]]): A dictionary containing descriptions, lower and upper limits, and units for each parameter.

    Returns:
        Dict[str, float]: A dictionary of user-inputted values, validated within the defined limits.
    """
    parameters = {}
    for symbol, limit in limits.items():
        value = st.text_input(f"Enter {limit['desc']} ({symbol}) [{limit['unit']}]:", value=limit['lower'])

        if value:
            try:
                value = float(value)
                if not (limit['lower'] <= value <= limit['upper']):
                    st.error(f"Please enter a value between {limit['lower']} and {limit['upper']} {limit['unit']}.")
                else:
                    st.success(f"Value accepted: {value} {limit['unit']}")
                    parameters[symbol] = value
            except ValueError:
                st.error("Please enter a valid number.")

    return parameters


def AC_model_klinesmith2007(article_identifier: str) -> Tuple[KlineSmith2007Model, float]:
    """
    Executes the Klinesmith 2007 corrosion model.

    Returns:
        Tuple[KlineSmith2007Model, float]: An instance of the KlineSmith2007Model class and the duration for which the model is evaluated.
    """
    time = st.number_input('Enter duration [years]:', min_value=2.5, max_value=100.0, step=2.5)

    limits = {
        'T': {'desc': 'Temperature', 'lower': -17.1, 'upper': 28.7, 'unit': '°C'},
        'TOW': {'desc': 'Time of Wetness', 'lower': 0.01, 'upper': 1.0, 'unit': 'annual fraction'},
        'SO2': {'desc': 'SO₂ Deposit', 'lower': 0.7, 'upper': 150.4, 'unit': 'mg/(m²⋅d)'},
        'Cl': {'desc': 'Cl⁻ Deposit', 'lower': 0.4, 'upper': 760.5, 'unit': 'mg/(m²⋅d)'}
    }

    parameters = get_parameters(limits)

    return KlineSmith2007Model(parameters), time
