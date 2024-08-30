import pandas as pd
import streamlit as st
import numpy as np
from typing import Dict, Tuple
from .corrosion_model import CorrosionModel


class Ma2010Model(CorrosionModel):
    """
    A corrosion model based on the study by Ma et al. (2010) which evaluates the atmospheric corrosion kinetics
    of low carbon steel in a tropical marine environment.

    Reference:
        Ma, Yuantai, Li, Ying, and Wang, Fuhui.
        "The atmospheric corrosion kinetics of low carbon steel in a tropical marine environment."
        Corrosion Science, 52(5), 1796-1800 (2010). Elsevier.
    """

    def __init__(self, parameters: Dict[str, float]):
        super().__init__(
            model_name='The Atmospheric Corrosion Kinetics of Low Carbon Steel in a Tropical Marine Environment')
        self.steel = "Low Carbon Steel (Q235)"
        self.parameters = parameters
        self.article_identifier = "ma2010"

    def eval_material_loss(self, time: float) -> float:
        """Calculates the material loss over time based on the provided environmental parameters."""

        # Define the distance points and their corresponding log(A) and n values
        distances = [25, 95, 375]
        log_A_site_I = [0.13548, 0.52743, 0.44306]
        n_site_I = [2.86585, 2.18778, 1.55029]
        log_A_site_II = [1.5095, 1.5981, 1.26836]
        n_site_II = [1.15232, 1.05915, 0.76748]

        if self.parameters['corrosion_site'] == 1:
            log_A_values = log_A_site_I
            n_values = n_site_I
        elif self.parameters['corrosion_site'] == 2:
            log_A_values = log_A_site_II
            n_values = n_site_II

        for i in range(len(distances) - 1):
            if distances[i] <= self.parameters['distance'] <= distances[i + 1]:
                log_A = log_A_values[i] + (log_A_values[i + 1] - log_A_values[i]) * \
                        (self.parameters['distance'] - distances[i]) / (distances[i + 1] - distances[i])
                n = n_values[i] + (n_values[i + 1] - n_values[i]) * \
                    (self.parameters['distance'] - distances[i]) / (distances[i + 1] - distances[i])
                A = np.exp(log_A)
                return A * time ** n

        if self.parameters['distance'] == distances[0]:
            A, n = np.exp(log_A_values[0]), n_values[0]
        elif self.parameters['distance'] == distances[-1]:
            A, n = np.exp(log_A_values[-1]), n_values[-1]

        return A * time ** n


def get_parameters(article_identifier: str, limits: Dict[str, Dict[str, float]]) -> Dict[str, float]:
    """
    Loads data, retrieves the corrosion site, and gathers parameters required for the corrosion model based on user input.

    Args:
        article_identifier (str): The identifier for the article.
        limits (Dict[str, Dict[str, float]]): A dictionary containing parameter limits and descriptions.

    Returns:
        Dict[str, float]: A dictionary of parameters with their user-provided values.
    """
    # Load data
    table_2 = pd.read_csv(f'../data/tables/{article_identifier}_tables_table_2.csv', header=None)

    # Initialize parameters dictionary
    parameters = {}

    # Display the corrosion site selection box
    st.table(table_2)
    corrosion_site = st.selectbox('Select corrosion site:', table_2.iloc[1:, 0])
    parameters['corrosion_site'] = int(table_2.iloc[1:, 0].tolist().index(corrosion_site) + 1)

    # Collect user inputs for other parameters
    for symbol, limit in limits.items():
        value = st.text_input(f"Enter {limit['desc']} ({symbol}) [{limit['unit']}]:", value=limit['lower'])

        if value:
            try:
                value = float(value)
                if not (limit['lower'] <= value <= limit['upper']):
                    st.error(f"Please enter a value between {limit['lower']} and {limit['upper']} {limit['unit']}.")
                else:
                    st.success(f"Value accepted: {value} {limit['unit']}")
                    # Map 'D' to 'distance'
                    if symbol == 'D':
                        parameters['distance'] = value
                    else:
                        parameters[symbol] = value
            except ValueError:
                st.error("Please enter a valid number.")
        else:
            if symbol == 'D':
                parameters['distance'] = limit['lower']  # Assign a default value if no input is provided
            else:
                parameters[symbol] = limit['lower']

    return parameters



def AC_model_ma2010(article_identifier: str) -> Tuple[Ma2010Model, float]:
    """
    Executes the Ma 2010 corrosion model.

    Returns:
        Tuple[Ma2010Model, float]: An instance of the TropicalMarineEnvironmentModel class
                                                      and the duration for which the model is evaluated.
    """
    time = st.number_input('Enter duration [years]:', min_value=2.5, max_value=100.0, step=2.5)
    limits = {'D': {'desc': 'Distance', 'lower': 25, 'upper': 375, 'unit': 'm'}}

    parameters = get_parameters("ma2010", limits)

    return Ma2010Model(parameters), time
