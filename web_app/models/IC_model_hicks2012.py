import pandas as pd
import streamlit as st
import numpy as np
from typing import Dict, Optional
from .corrosion_model import CorrosionModel

class Hicks2012Model(CorrosionModel):
    """
    A corrosion model based on the study by Hicks and Oster (2012) which predicts the risk of accelerated
    corrosion to port infrastructure due to various water quality parameters.

    Reference:
        Hicks, Randall E., and Ryan J. Oster.
        "Developing a risk assessment tool to predict the risk of accelerated corrosion to port infrastructure."
        Great Lakes Maritime Research Institute, 2012.
    """

    def __init__(self, parameters: Optional[Dict[str, float]] = None):
        super().__init__(model_name='Risk Assessment Tool for Accelerated Corrosion in Port Infrastructure')
        self.steel = "A328 Sheet Steel"
        self.parameters = parameters if parameters else self._get_parameters()
        self._display_reference_values()

    def _get_parameters(self) -> Dict[str, float]:
        """Prompts the user to input values for all parameters and returns a dictionary of the parameters."""
        parameters = {
            'Alkalinity': st.number_input(r'Enter the Alkalinity [$mg L^{-1}$]:', min_value=0.0, value=0.1, step=0.1, key="alkalinity"),
            'Chloride': st.number_input(r'Enter the Chloride content [$mg L^{-1}$]:', min_value=0.0, value=0.1, step=0.1, key="chloride"),
            'Sulfate': st.number_input(r'Enter the Sulfate content [$mg L^{-1}$]:', min_value=0.0, value=0.1, step=0.1, key="sulfate"),
            'Larson Skold Index': st.number_input(r'Enter the Larson Skold Index:', min_value=0.0, value=0.1, step=0.1, key="larson_skold"),
            'Conductivity': st.number_input(r'Enter the Conductivity [$\mu D cm^{-1}$]:', min_value=0.0, value=0.1, step=0.1, key="conductivity"),
            'pH': st.number_input(r'Enter the pH:', min_value=0.0, value=7.0, step=0.1, key="ph"),
            'Dissolved Oxygen': st.number_input(r'Enter the Dissolved Oxygen content [$mg L^{-1}$]:', min_value=0.0, value=0.1, step=0.1, key="dissolved_oxygen"),
            'Dissolved Organic Carbon': st.number_input(r'Enter the Dissolved Organic Carbon content [$mg L^{-1}$]:', min_value=0.0, value=0.1, step=0.1, key="dissolved_organic_carbon"),
            'Dissolved Copper': st.number_input(r'Enter the Dissolved Copper content [$mg L^{-1}$]:', min_value=0.0, value=0.1, step=0.1, key="dissolved_copper")
        }

        return parameters

    def _display_reference_values(self) -> None:
        """Displays the reference values related to the study."""
        with st.expander("Reference Values"):
            # Display relevant data tables
            st.title('Statistical relationship between the long-term rate of steel corrosion (mm/yr) and various water quality parameters measured during 2010 at ten sites in the Duluth-Superior Harbor.')
            st.table(pd.read_csv('../data/tables/hicks2012_table_2.csv'))

            st.title('Water quality measurements made from 9-10 August 2010 in the Duluth-Superior Harbor.')
            st.table(pd.read_csv('../data/tables/hicks2012_table_7.csv'))

            st.title('Water quality measurements made from 26-27 July 2011 in the Duluth-Superior Harbor and three harbors on the north shore of Lake Superior.')
            st.table(pd.read_csv('../data/tables/hicks2012_table_8.csv'))

    def eval_material_loss(self, time: float) -> float:
        """
        Evaluates the material loss over time based on the provided parameters.

        Args:
            time (float): The time duration in years.

        Returns:
            float: The calculated material loss.
        """
        # Define the parameters and their formulas
        parameter_formulas = {
            'Alkalinity': (0.0014, -0.0103),
            'Chloride': (0.0055, 0.0382),
            'Sulfate': (0.0008, 0.0735),
            'Larson Skold Index': (0.0372, 0.0751),
            'Conductivity': (0.0004, 0.0052),
            'pH': (-0.0155, 0.2113),
            'Dissolved Organic Carbon': (0.0016, 0.0683),
            'Dissolved Copper': (3.785, 0.0803),
            'Dissolved Oxygen': (-0.0151, 0.2306),
        }

        # Calculate the d_values based on the input parameters
        d_values = {
            f'd_{key.replace(" ", "_")}': (multiplier * self.parameters[key] + constant) if self.parameters[key] != 0 else 0
            for key, (multiplier, constant) in parameter_formulas.items()
        }

        # Sum up the d_values to calculate the corrosion rate
        corrosion_rate = sum(d_values.values())

        # Calculate the material loss over time
        material_loss = corrosion_rate * time

        return material_loss

