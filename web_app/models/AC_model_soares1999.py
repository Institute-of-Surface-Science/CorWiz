import streamlit as st
import numpy as np
from typing import Dict, Optional
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

    def __init__(self, parameters: Optional[Dict[str, float]] = None):
        super().__init__(model_name='Reliability of Maintained, Corrosion Protected Plates')
        self.steel = "Steel"
        self.parameters = parameters if parameters else self._get_parameters()

    def _get_parameters(self) -> Dict[str, float]:
        """Prompts the user to input values for all parameters and returns a dictionary of the parameters."""
        limits = {
            'd_inf': {'desc': 'Long term thickness of corrosion wastage', 'lower': 0.001, 'upper': 1000, 'unit': 'mm'},
            't_c': {'desc': 'Coating life', 'lower': 0.01, 'upper': 100, 'unit': 'years'},
            't_t': {'desc': 'Transition time', 'lower': 0.01, 'upper': 100, 'unit': 'years'}
        }

        parameters = {}
        for symbol, limit in limits.items():
            value = st.number_input(
                f"Enter {limit['desc']} ({symbol}) [{limit['unit']}]:",
                min_value=float(limit['lower']),
                max_value=float(limit['upper']),
                value=float(limit['lower']),
                step=0.01 if 'mm' in limit['unit'] else 1.0,
                key=f"input_{symbol}"
            )
            parameters[symbol] = value

        return parameters

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

