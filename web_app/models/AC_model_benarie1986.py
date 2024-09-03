import pandas as pd
import streamlit as st
import numpy as np
from typing import Dict
from .corrosion_model import CorrosionModel


class Benarie1986Model(CorrosionModel):
    """
    A corrosion model based on the research by Benarie and Lipfert (1986) which predicts material loss over time.

    Reference:
        Benarie, Michel, and Frederick L. Lipfert.
        "A general corrosion function in terms of atmospheric pollutant concentrations and rain pH."
        Atmospheric Environment (1967) 20, no. 10 (1986): 1947-1958. Elsevier.
    """

    DATA_FILE_PATH = '../data/tables/benarie1986_tables_table_2.csv'
    DEFAULT_CORROSION_SITE_KEY = 'corrosion_site'

    def __init__(self):
        super().__init__(model_name='Benarie1986 Corrosion Model')
        self.parameters: Dict[str, float] = {}
        self.table_2 = self._load_data()

    def _load_data(self) -> pd.DataFrame:
        """Loads the relevant data for the model."""
        return pd.read_csv(self.DATA_FILE_PATH, header=None)

    def display_parameters(self) -> None:
        """Displays the parameters selection interface for the user."""
        corrosion_sites = self.table_2.iloc[1:, 0]
        selected_site = st.selectbox('Select corrosion site:', corrosion_sites)
        corrosion_site_index = corrosion_sites.tolist().index(selected_site) + 1
        self.parameters[self.DEFAULT_CORROSION_SITE_KEY] = corrosion_site_index
        self._display_site_info(corrosion_site_index)

    def _display_site_info(self, corrosion_site: int) -> None:
        """Displays detailed information about the selected corrosion site."""
        site_info = self.table_2.iloc[corrosion_site, :5]
        site_name, weight_loss, exponent, so2_cl_deposits, ph_value = site_info

        st.markdown(f"### Selected Site: **{site_name}**")
        st.markdown(
            f"""
            The following parameters have been selected for the site **{site_name}**. These parameters are used in the corrosion model to predict the material loss over time.

            **Weight Loss per Wetness Year ($A$):**
            - The rate of material loss due to corrosion, expressed in micrometers per year (\u03BCm/year).  
            - **Value:** {weight_loss} \u03BCm/year

            **Exponent ($b$):**
            - The exponent used in the corrosion rate equation, which modifies the time dependency of the corrosion process.
            - **Value:** {exponent}

            **$SO_2$ + $Cl^-$ Deposits:**
            - The combined deposition rate of sulfur dioxide and chloride ions, expressed in milligrams per square meter per day (mg/m²/day). This value reflects the environmental aggressiveness.
            - **Value:** {so2_cl_deposits} mg/m²/day

            **$pH$ of the Environment:**
            - The acidity or alkalinity of the environment, which can significantly influence the corrosion rate.
            - **Value:** {ph_value}
            """
        )

    def evaluate_material_loss(self, time: float) -> np.ndarray:
        """
        Calculates and returns the material loss over time for the selected corrosion site.

        This method also retrieves the necessary parameters (corrosion speed and exponent)
        for the calculation based on the selected site.
        """
        site_index = self.parameters[self.DEFAULT_CORROSION_SITE_KEY]
        A = float(self.table_2.iloc[site_index, 1])
        n = float(self.table_2.iloc[site_index, 2])
        return A * time ** n
