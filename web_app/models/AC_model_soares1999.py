import streamlit as st
import numpy as np
from typing import Dict, Tuple
from .corrosion_model import CorrosionModel


class Soares1999Model(CorrosionModel):
    """
    A corrosion model based on the study by Soares and Garbatov (1999) which evaluates the material loss
    of maintained, corrosion-protected steel plates subjected to non-linear corrosion and compressive loads.

    Reference:
        Soares, C. Guedes, and Yordan Garbatov.
        "Reliability of maintained, corrosion protected plates subjected to non-linear corrosion and compressive loads."
        Marine Structures, 12(6), 425-445 (1999). Elsevier.
    """

    def __init__(self, parameters: Dict[str, float]):
        super().__init__(model_name='Reliability of Maintained, Corrosion Protected Plates')
        self.steel = "Steel"
        self.parameters = parameters
        self.article_identifier = "soares1999"

    def eval_material_loss(self, time: np.ndarray) -> np.ndarray:
        """
        Evaluates the material loss over time based on the provided parameters.

        Args:
            time (np.ndarray): Array of time values in years.

        Returns:
            np.ndarray: Array of material loss values corresponding to each time point.
        """
        material_loss = np.zeros_like(time)
        mask = time >= self.parameters['t_c']
        material_loss[mask] = self.parameters['d_inf'] * (
                1 - np.exp(-(time[mask] - self.parameters['t_c']) / self.parameters['t_t'])
        )
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
                parameters[symbol] = limit['lower']
        else:
            parameters[symbol] = limit['lower']

    return parameters


def AC_model_soares1999(article_identifier: str) -> Tuple[Soares1999Model, float]:
    """
    Executes the Soares 1999 corrosion model.

    Returns:
        Tuple[Soares1999Model, float]: An instance of the CoatedMassLossModel class and the duration for which the model is evaluated.
    """
    time = st.number_input('Enter duration [years]:', min_value=2.5, max_value=100.0, step=2.5)

    limits = {
        'd_inf': {'desc': 'Long term thickness of corrosion wastage', 'lower': 0.001, 'upper': 1000, 'unit': 'mm'},
        't_c': {'desc': 'Coating life', 'lower': 0, 'upper': 100, 'unit': 'years'},
        't_t': {'desc': 'Transition time', 'lower': 0, 'upper': 100, 'unit': 'years'}
    }

    parameters = get_parameters(limits)

    return Soares1999Model(parameters), time
