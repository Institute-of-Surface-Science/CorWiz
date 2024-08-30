import pandas as pd
import streamlit as st
import numpy as np
from typing import Tuple, Optional
from .corrosion_model import CorrosionModel

class Benarie1986Model(CorrosionModel):
    """
    A corrosion model based on the research by Benarie and Lipfert (1986) which predicts material loss over time.

    Reference:
        Benarie, Michel, and Frederick L. Lipfert.
        "A general corrosion function in terms of atmospheric pollutant concentrations and rain pH."
        Atmospheric Environment (1967) 20, no. 10 (1986): 1947-1958. Elsevier.
    """

    def __init__(self, parameters: dict):
        super().__init__(model_name='Benarie1986 Corrosion Model')
        self.steel = "Carbon Steel"
        self.parameters = parameters
        self.article_identifier = "benarie1986"
        self.table_2 = self._load_data()

    def _load_data(self) -> pd.DataFrame:
        """Loads the relevant data table for the Benarie1986 model."""
        data_path = f'../data/tables/{self.article_identifier}_tables_table_2.csv'
        return pd.read_csv(data_path, header=None)

    def select_corrosion_site(self) -> int:
        """Displays a selection box for corrosion sites and returns the selected site index."""
        corrosion_sites = self.table_2.iloc[1:, 0]
        selected_site = st.selectbox('Select corrosion site:', corrosion_sites)
        return corrosion_sites.tolist().index(selected_site) + 1

    def display_site_info(self, corrosion_site: int) -> None:
        """Displays detailed information about the selected corrosion site in a structured and informative Markdown format."""
        site_name = self.table_2.iloc[corrosion_site, 0]
        weight_loss = self.table_2.iloc[corrosion_site, 1]
        exponent = self.table_2.iloc[corrosion_site, 2]
        so2_cl_deposits = self.table_2.iloc[corrosion_site, 3]
        ph_value = self.table_2.iloc[corrosion_site, 4]

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

    def eval_corrosion_speed_and_exponent(self) -> Tuple[float, float]:
        """Calculates and returns the corrosion speed (A) and exponent (b) for the selected site."""
        A = float(self.table_2.iloc[self.parameters['corrosion_site'], 1])
        b = float(self.table_2.iloc[self.parameters['corrosion_site'], 2])
        return A, b

    def eval_material_loss(self, time: float) -> np.ndarray:
        """Calculates and returns the material loss over time for the selected corrosion site."""
        A, n = self.eval_corrosion_speed_and_exponent()
        return A * time ** n


# TODO: remove article_identifier
def AC_model_benarie1986(article_identifier: str) -> Tuple[Benarie1986Model, float]:
    """
    Executes the Benarie1986 corrosion model.

    Returns:
        Tuple[Benarie1986Model, float]: An instance of the Benarie1986Model class and the duration for which the model is evaluated.

    Reference:
        Benarie, Michel, and Frederick L. Lipfert.
        "A general corrosion function in terms of atmospheric pollutant concentrations and rain pH."
        Atmospheric Environment (1967) 20, no. 10 (1986): 1947-1958. Elsevier.
    """
    time_duration = st.number_input('Enter duration [years]:', min_value=2.5, max_value=100.0, step=2.5)
    model = Benarie1986Model(parameters={})

    corrosion_site = model.select_corrosion_site()
    model.parameters['corrosion_site'] = corrosion_site

    model.display_site_info(corrosion_site)

    return model, time_duration
