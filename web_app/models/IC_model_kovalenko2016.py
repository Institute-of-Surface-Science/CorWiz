import pandas as pd
import streamlit as st
from typing import Dict, Optional
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

    DATA_FILE_PATH = '../data/tables/kovalenko2016_tables_table_3.csv'

    def __init__(self, parameters: Optional[Dict[str, float]] = None):
        super().__init__(model_name='Long-term Immersion Corrosion of Steel in Variable Seawater Conditions')
        self.parameters = parameters if parameters else self._get_parameters()

    def _get_parameters(self) -> Dict[str, float]:
        """Prompts the user to input values for all parameters and returns a dictionary of the parameters."""
        table = pd.read_csv(self.DATA_FILE_PATH, header=None)

        # Display the condition reference table
        self.display_condition_reference_table(table)

        # Select condition based on user input
        condition_index = st.selectbox('Select the Temperature and Dissolved Inorganic Nitrogen condition:', table.iloc[1:, 0])
        condition_index = int(condition_index)

        # Extract the relevant parameters based on the selected condition
        parameters = {
            'c_s': float(table.iloc[condition_index, 3]),
            'r_s': float(table.iloc[condition_index, 4])
        }

        return parameters

    def display_condition_reference_table(self, table: pd.DataFrame) -> None:
        """Displays the condition reference table."""
        with st.expander("Condition Reference Table"):
            st.table(table.iloc[:, 1:-2])

    def eval_material_loss(self, time: float) -> float:
        """
        Evaluates the material loss over time based on the provided parameters.

        Args:
            time (float): The time duration in years.

        Returns:
            float: The calculated material loss.
        """
        return self.parameters['c_s'] + time * self.parameters['r_s']

