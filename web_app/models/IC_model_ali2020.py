import pandas as pd
import streamlit as st
import numpy as np
from typing import Dict, Tuple
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

    def __init__(self, parameters: Dict[str, float]):
        super().__init__(model_name='Empirical Prediction of Weight Change and Corrosion Rate of Low-Carbon Steel')
        self.steel = "Low carbon steel"
        self.parameters = parameters
        self.article_identifier = "ali2020"

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


def get_parameters(limits: Dict[str, Dict[str, float]]) -> Dict[str, float]:
    """
    Retrieves the parameters required for the corrosion model based on user input.

    Args:
        limits (Dict[str, Dict[str, float]]): A dictionary containing parameter limits and descriptions.

    Returns:
        Dict[str, float]: A dictionary of parameters with their user-provided values.
    """
    parameters = {}
    for symbol, limit in limits.items():
        value = st.text_input(f"${symbol}$ - Enter {limit['desc']}  [ ${limit['unit']}$ ]:", value=limit['lower'])

        if value:
            try:
                value = float(value)
                if not (limit['lower'] <= value <= limit['upper']):
                    st.error(f"Please enter a value between {limit['lower']} and {limit['upper']} ${limit['unit']}$")
                else:
                    st.success(f"Value accepted: {value} ${limit['unit']}$")
                    parameters[symbol] = value
            except ValueError:
                st.error("Please enter a valid number.")
                parameters[symbol] = limit['lower']
        else:
            parameters[symbol] = limit['lower']

    return parameters


def IC_model_ali2020(article_identifier: str) -> Tuple[Ali2010Model, float]:
    """
    Executes the Ali 2020 corrosion model.

    Returns:
        Tuple[Ali2010Model, float]: An instance of the EmpiricalPredictionModel class and the duration for which the model is evaluated.
    """
    time = st.number_input('Enter duration [years]:', min_value=1.0, max_value=100.0, step=0.1)

    limits = {
        'C': {'desc': 'Concentration of NaCl', 'lower': 0.0, 'upper': 5.0, 'unit': '%w/w'},
    }

    parameters = get_parameters(limits)

    # Load the data and calculate 'b' directly
    table_3 = pd.read_csv('../data/tables/ali2020_tables_table_3.csv', header=None)
    nacl_concs = np.array(table_3.iloc[1:, 0].astype(float))
    constants = np.array(table_3.iloc[1:, 2].astype(float))

    # Interpolate or get the exact 'b' value
    if parameters['C'] in nacl_concs:
        parameters['b'] = constants[nacl_concs == parameters['C']][0]
    else:
        parameters['b'] = np.interp(parameters['C'], nacl_concs, constants)

    st.write(r'Mass loss due to corrosion, $W_L [\mu m] = (0.00006C + 0.0008)t + b $')

    return Ali2010Model(parameters), time
