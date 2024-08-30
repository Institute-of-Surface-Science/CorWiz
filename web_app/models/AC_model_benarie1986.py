import pandas as pd
import streamlit as st
import numpy as np
from typing import Tuple, Optional
from .corrosion_model import CorrosionModel

class GeneralCorrosionModel(CorrosionModel):
    """
    A general corrosion function in terms of atmospheric pollutant concentrations and rain pH.

    This model is based on the research by Benarie and Lipfert (1986) and predicts material loss over time.

    Reference:
        Benarie, Michel, and Frederick L. Lipfert.
        "A general corrosion function in terms of atmospheric pollutant concentrations and rain pH."
        Atmospheric Environment (1967) 20, no. 10 (1986): 1947-1958. Elsevier.
    """

    def __init__(self, parameters: dict, article_identifier: str):
        super().__init__()
        self.model_name = 'A general corrosion function in terms of atmospheric pollutant concentrations and rain pH'
        self.article_identifier = article_identifier
        self.steel = "Carbon Steel"
        self.parameters = parameters
        self.table_2 = self._load_data()

    def _load_data(self) -> pd.DataFrame:
        """Loads the relevant data table based on the article identifier."""
        data_path = f'../data/tables/{self.article_identifier}_tables_table_2.csv'
        return pd.read_csv(data_path, header=None)

    def select_corrosion_site(self) -> int:
        """Displays a selection box for corrosion sites and returns the selected site index."""
        corrosion_sites = self.table_2.iloc[1:, 0]
        selected_site = st.selectbox('Select corrosion site:', corrosion_sites)
        return corrosion_sites.tolist().index(selected_site) + 1

    def display_site_info(self, corrosion_site: int) -> None:
        """Displays information about the selected corrosion site."""
        st.write(f'Selected site: {self.table_2.iloc[corrosion_site, 0]}')
        st.write(f'Weight loss per wetness year, $A$ = {self.table_2.iloc[corrosion_site, 1]}')
        st.write(f'Exponent, $b$ = {self.table_2.iloc[corrosion_site, 2]}')
        st.write(f'$SO_2$ + $Cl^-$ deposits [$mg m^{-2} d^{-1}$] = {self.table_2.iloc[corrosion_site, 3]}')
        st.write(f'$pH$ = {self.table_2.iloc[corrosion_site, 4]}')

    def eval_corrosion_speed_and_exponent(self) -> Tuple[float, float]:
        """Evaluates and returns the corrosion speed (A) and exponent (b) for the selected site."""
        A = float(self.table_2.iloc[self.parameters['corrosion_site'], 1])
        b = float(self.table_2.iloc[self.parameters['corrosion_site'], 2])
        return A, b

    def eval_material_loss(self, time: float) -> np.ndarray:
        """Evaluates and returns the material loss over time."""
        A, n = self.eval_corrosion_speed_and_exponent()
        return A * time ** n


def AC_model_benarie1986(article_identifier: str) -> Tuple[GeneralCorrosionModel, float]:
    """
    Runs the Benarie 1986 corrosion model using the specified article identifier.

    Args:
        article_identifier (str): The identifier for the article and data tables.

    Returns:
        Tuple[GeneralCorrosionModel, float]: An instance of the GeneralCorrosionModel class and the duration for which the model is evaluated.

    Reference:
        Benarie, Michel, and Frederick L. Lipfert.
        "A general corrosion function in terms of atmospheric pollutant concentrations and rain pH."
        Atmospheric Environment (1967) 20, no. 10 (1986): 1947-1958. Elsevier.
    """
    time_duration = st.number_input('Enter duration [years]:', min_value=1.0, max_value=100.0, step=0.1)
    model = GeneralCorrosionModel(parameters={}, article_identifier=article_identifier)

    corrosion_site = model.select_corrosion_site()
    model.parameters['corrosion_site'] = corrosion_site

    model.display_site_info(corrosion_site)

    return model, time_duration
