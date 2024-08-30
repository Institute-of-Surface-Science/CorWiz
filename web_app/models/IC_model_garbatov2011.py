import pandas as pd
import streamlit as st
import numpy as np
from typing import Dict, Tuple
from .corrosion_model import CorrosionModel


class Garbatov2011Model(CorrosionModel):
    """
    A corrosion model based on the study by Garbatov et al. (2011) which predicts material loss
    in marine structures.

    Reference:
        Garbatov, Y., Zayed, A., and Soares, C. Guedes.
        "Corrosion modeling in marine structures."
        Marine Technology and Engineering, 2011.
    """

    def __init__(self, parameters: Dict[str, float]):
        super().__init__(model_name='Corrosion Modeling in Marine Structures')
        self.steel = "Mild Carbon Steel"
        self.parameters = parameters
        self.article_identifier = "garbatov2011"

    def eval_material_loss(self, time: float) -> float:
        """
        Evaluates the material loss over time based on the provided parameters.

        Args:
            time (float): The time duration in years.

        Returns:
            float: The calculated material loss.
        """
        # Calculate the effects of temperature, dissolved oxygen concentration, and flow velocity
        d_temperature = 0.0014 * self.parameters['Temperature'] + 0.0154
        f_temperature = self.parameters['Temperature'] / 15.5

        d_dissolved_oxygen = 0.0268 * self.parameters['Dissolved Oxygen Concentration'] + 0.0086
        f_dissolved_oxygen = 0.9483 * self.parameters['Dissolved Oxygen Concentration'] + 0.0517

        d_flow_velocity = 0.9338 * (1 - np.exp(-0.4457 * (self.parameters['Flow Velocity'] + 0.2817)))
        f_flow_velocity = 1.0978 * (1 - np.exp(-2.2927 * (self.parameters['Flow Velocity'] + 0.0548)))

        # Calculate the nominal corrosion rate
        nominal_corrosion_rate = d_temperature + d_dissolved_oxygen + d_flow_velocity

        # Calculate the overall corrosion rate
        corrosion_rate = f_temperature * f_dissolved_oxygen * f_flow_velocity * nominal_corrosion_rate

        # Calculate the material loss over time
        material_loss = corrosion_rate * time

        return material_loss


def IC_model_garbatov2011() -> Tuple[Garbatov2011Model, float]:
    """
    Executes the Garbatov 2011 corrosion model.

    Returns:
        Tuple[Garbatov2011Model, float]: An instance of the Garbatov2011Model class and the duration for which the model is evaluated.
    """
    time = st.number_input('Enter duration [years]:', min_value=1.0, max_value=100.0, step=0.1)

    parameters = {
        'Temperature': st.number_input('Enter the Temperature [°C]:', min_value=-10.0, max_value=50.0, value=20.0, step=0.1),
        'Dissolved Oxygen Concentration': st.number_input('Enter the Dissolved Oxygen Concentration [ml/l]:', min_value=0.0, max_value=14.6, value=6.0, step=0.1),
        'Flow Velocity': st.number_input('Enter the Flow Velocity [m/s]:', min_value=0.0, max_value=10.0, value=1.0, step=0.1)
    }

    return Garbatov2011Model(parameters), time
