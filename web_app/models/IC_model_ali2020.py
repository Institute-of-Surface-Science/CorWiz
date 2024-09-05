import pandas as pd
import streamlit as st
import numpy as np
from typing import Dict, Optional
from .corrosion_model import CorrosionModel

class Ali2010Model(CorrosionModel):
    """
    A corrosion model based on the study by Ali and Fulazzaky (2020) which predicts the weight change
    and corrosion rate of low-carbon steel.

    Reference:
        Ali, Nurdin, and Mohamad Ali Fulazzaky.
        "The empirical prediction of weight change and corrosion rate of low-carbon steel."
        Heliyon, 6(9), e05050 (2020). Elsevier.
    """

    DATA_FILE_PATH = '../data/tables/ali2020_tables_table_3.csv'

    def __init__(self, json_file_path: str):
        super().__init__(json_file_path=json_file_path, model_name='Ali2010Model')
        self.parameters: Dict[str, float] = {}
        self.table_3 = self._load_data()

    def _load_data(self) -> pd.DataFrame:
        """Loads the relevant data table for the Ali2010 model."""
        return pd.read_csv(self.DATA_FILE_PATH, header=None)

    def display_parameters(self) -> None:
        """Prompts the user to input values for all parameters and calculates the parameter 'b'."""
        limits = {
            'C': {'desc': 'Concentration of NaCl', 'lower': 0.0, 'upper': 5.0, 'unit': '%w/w'},
        }

        for symbol, limit in limits.items():
            self.parameters[symbol] = st.number_input(
                f"${symbol}$ - Enter {limit['desc']} [${limit['unit']}$]:",
                min_value=float(limit['lower']),
                max_value=float(limit['upper']),
                value=float(limit['lower']),
                step=0.01,
                key=f"input_{symbol}"
            )

        # Interpolate or get the exact 'b' value based on the user input for 'C'
        nacl_concs = np.array(self.table_3.iloc[1:, 0].astype(float))
        constants = np.array(self.table_3.iloc[1:, 2].astype(float))

        if self.parameters['C'] in nacl_concs:
            self.parameters['b'] = constants[nacl_concs == self.parameters['C']][0]
        else:
            self.parameters['b'] = np.interp(self.parameters['C'], nacl_concs, constants)

        st.write(r'Mass loss due to corrosion, $W_L [\mu m] = (0.00006C + 0.0008)t + b $')

    def evaluate_material_loss(self, time: float) -> float:
        """
        Evaluates the material loss over time based on the provided parameters.

        Args:
            time (float): The time duration in years.

        Returns:
            float: The calculated material loss.
        """
        material_loss = (0.00006 * self.parameters['C'] + 0.0008) * (time*365*24) + self.parameters['b']
        return material_loss
