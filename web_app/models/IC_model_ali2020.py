import pandas as pd
import streamlit as st
import numpy as np
from typing import Dict, Tuple, Optional
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

    def __init__(self, parameters: Optional[Dict[str, float]] = None):
        super().__init__(model_name='Empirical Prediction of Weight Change and Corrosion Rate of Low-Carbon Steel')
        self.parameters = parameters if parameters else self._get_parameters()

    def _get_parameters(self) -> Dict[str, float]:
        """Prompts the user to input values for all parameters and returns a dictionary of the parameters."""
        limits = {
            'C': {'desc': 'Concentration of NaCl', 'lower': 0.0, 'upper': 5.0, 'unit': '%w/w'},
        }

        parameters = {}
        for symbol, limit in limits.items():
            value = st.number_input(
                f"${symbol}$ - Enter {limit['desc']} [${limit['unit']}$]:",
                min_value=float(limit['lower']),
                max_value=float(limit['upper']),
                value=float(limit['lower']),
                step=0.01,
                key=f"input_{symbol}"
            )
            parameters[symbol] = value

        # Load the data and calculate 'b'
        table_3 = pd.read_csv(self.DATA_FILE_PATH, header=None)
        nacl_concs = np.array(table_3.iloc[1:, 0].astype(float))
        constants = np.array(table_3.iloc[1:, 2].astype(float))

        # Interpolate or get the exact 'b' value
        if parameters['C'] in nacl_concs:
            parameters['b'] = constants[nacl_concs == parameters['C']][0]
        else:
            parameters['b'] = np.interp(parameters['C'], nacl_concs, constants)

        st.write(r'Mass loss due to corrosion, $W_L [\mu m] = (0.00006C + 0.0008)t + b $')

        return parameters

    def eval_material_loss(self, time: float) -> float:
        """
        Evaluates the material loss over time based on the provided parameters.

        Args:
            time (float): The time duration in years.

        Returns:
            float: The calculated material loss.
        """
        material_loss = (0.00006 * self.parameters['C'] + 0.0008) * time + self.parameters['b']
        return material_loss


# Example of usage
def run_ali2020_model() -> Tuple[Ali2010Model, float]:
    """
    Runs the Ali 2020 corrosion model.

    Returns:
        Tuple[Ali2010Model, float]: An instance of the Ali2010Model class and the duration for which the model is evaluated.
    """
    time_duration = st.number_input('Enter duration [years]:', min_value=1.0, max_value=100.0, step=0.1, key="duration")
    model = Ali2010Model()

    return model, time_duration
