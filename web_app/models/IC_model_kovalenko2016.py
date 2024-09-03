import pandas as pd
import streamlit as st
import numpy as np
from typing import Dict, Tuple
from .corrosion_model import CorrosionModel


class Kovalenko2016Model(CorrosionModel):
    """
    A corrosion model based on the study by Kovalenko et al. (2016) which evaluates long-term immersion corrosion
    of steel subjected to large annual variations in seawater temperature and nutrient concentration.

    Reference:
        Kovalenko, Roman, Robert E. Melchers, and Boris Chernov.
        "Long-term immersion corrosion of steel subject to large annual variations in seawater temperature and nutrient concentration."
        Structure and Infrastructure Engineering, 13(8), 978-987 (2016). Informa UK Limited.
    """

    def __init__(self, parameters: Dict[str, float]):
        super().__init__(model_name='Long-term Immersion Corrosion of Steel in Variable Seawater Conditions')
        self.steel = "Mild Steel"
        self.parameters = parameters
        self.article_identifier = "kovalenko2016"

    def eval_material_loss(self, time: float) -> float:
        """
        Evaluates the material loss over time based on the provided parameters.

        Args:
            time (float): The time duration in years.

        Returns:
            float: The calculated material loss.
        """
        return self.parameters['c_s'] + time * self.parameters['r_s']


def get_parameters(article_identifier: str) -> Dict[str, float]:
    """
    Retrieves the parameters required for the Kovalenko 2016 corrosion model based on user input.

    Args:
        article_identifier (str): The identifier for the article.

    Returns:
        Dict[str, float]: A dictionary of parameters with their user-provided values.
    """
    # Load the data table
    table = pd.read_csv(f'../data/tables/{article_identifier}_tables_table_3.csv', header=None)

    with st.expander("Condition Reference Table"):
        st.table(table.iloc[:, 1:-2])

    # Select condition based on user input
    condition_index = st.selectbox('Select the Temperature and Dissolved Inorganic Nitrogen condition:', table.iloc[1:, 0])
    condition_index = int(condition_index)

    # Extract the relevant parameters based on the selected condition
    parameters = {
        'c_s': float(table.iloc[condition_index, 3]),
        'r_s': float(table.iloc[condition_index, 4])
    }

    return parameters


def IC_model_kovalenko2016() -> Tuple[Kovalenko2016Model, float]:
    """
    Executes the Kovalenko 2016 corrosion model.

    Returns:
        Tuple[Kovalenko2016Model, float]: An instance of the Kovalenko2016Model class and the duration for which the model is evaluated.
    """
    time = st.number_input('Enter duration [years]:', min_value=2.5, max_value=100.0, step=2.5)

    # Get parameters by loading the data and asking for user input
    parameters = get_parameters("kovalenko2016")

    return Kovalenko2016Model(parameters), time
