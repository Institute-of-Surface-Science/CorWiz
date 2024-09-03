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

    def __init__(self, json_file_path: str):
        super().__init__(json_file_path=json_file_path, model_name='Soares1999Model')
        self.parameters: Dict[str, float] = {}

    def display_parameters(self) -> None:
        """Prompts the user to input values for all parameters and stores them in the parameters dictionary."""
        limits = {
            'd_inf': {'desc': 'Long term thickness of corrosion wastage', 'lower': 0.001, 'upper': 1000, 'unit': 'mm'},
            't_c': {'desc': 'Coating life', 'lower': 0.01, 'upper': 100, 'unit': 'years'},
            't_t': {'desc': 'Transition time', 'lower': 0.01, 'upper': 100, 'unit': 'years'}
        }

        for symbol, limit in limits.items():
            self.parameters[symbol] = st.number_input(
                f"Enter {limit['desc']} ({symbol}) [{limit['unit']}]:",
                min_value=float(limit['lower']),
                max_value=float(limit['upper']),
                value=float(limit['lower']),
                step=0.01 if 'mm' in limit['unit'] else 1.0,
                key=f"input_{symbol}"
            )

    def evaluate_material_loss(self, time: np.ndarray) -> np.ndarray:
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
