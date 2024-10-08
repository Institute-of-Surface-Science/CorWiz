import pandas as pd
import streamlit as st
import numpy as np
from typing import Dict, Optional
from .corrosion_model import CorrosionModel

class Ma2010Model(CorrosionModel):
    """
    A corrosion model based on the study by Ma et al. (2010) which evaluates the atmospheric corrosion kinetics
    of low carbon steel in a tropical marine environment.

    Reference:
        Ma, Yuantai, Li, Ying, and Wang, Fuhui.
        "The atmospheric corrosion kinetics of low carbon steel in a tropical marine environment."
        Corrosion Science, 52(5), 1796-1800 (2010). Elsevier.
    """

    DATA_FILE_PATH = '../data/tables/ma2010_table_2.csv'
    COORDINATES_FILE_PATH = '../data/tables/ma2010_coordinates.csv'

    def __init__(self, json_file_path: str):
        super().__init__(json_file_path=json_file_path, model_name='Ma2010Model')
        self.parameters: Dict[str, float] = {}
        self.table_2 = self._load_data()

    def _load_data(self) -> pd.DataFrame:
        """Loads the relevant data table for the Ma2010 model."""
        return pd.read_csv(self.DATA_FILE_PATH, header=None)

    def display_parameters(self) -> None:
        """Prompts the user to input values for all parameters and returns a dictionary of the parameters."""
        st.table(self.table_2)
        corrosion_sites = self.table_2.iloc[1:, 0].tolist()
        corrosion_site = st.selectbox('Select corrosion site:', corrosion_sites)
        corrosion_site_index = corrosion_sites.index(corrosion_site) + 1

        limits = {'D': {'desc': 'Distance', 'lower': 25, 'upper': 375, 'unit': 'm'}}

        self.parameters = {
            'corrosion_site': corrosion_site_index,
        }
        limits = {'D': {'desc': 'Distance', 'lower': 25, 'upper': 375, 'unit': 'm'}}

        # Collect user input for the distance parameter
        for symbol, limit in limits.items():
            value = st.number_input(
                f"Enter {limit['desc']} ({symbol}) [{limit['unit']}]:",
                min_value=float(limit['lower']),
                max_value=float(limit['upper']),
                value=float(limit['lower']),
                step=0.01,
                key=f"input_{symbol}"
            )
            if symbol == 'D':
                self.parameters['distance'] = value

        # Add the selected location's coordinates to global MODEL_COORDINATES varaible
        coordinates = pd.read_csv(self.COORDINATES_FILE_PATH, header=None)
        coordinates = coordinates.iloc[self.parameters['corrosion_site'], 1:]
        self.model_coordinates = pd.DataFrame({
            'lat': [float(coordinates.iloc[0])],
            'lon': [float(coordinates.iloc[1])]
        })

    def evaluate_material_loss(self, time: float) -> float:
        """Calculates the material loss over time based on the provided environmental parameters."""

        # Define the distance points and their corresponding log(A) and n values
        distances = [25, 95, 375]
        log_A_site_I = [0.13548, 0.52743, 0.44306]
        n_site_I = [2.86585, 2.18778, 1.55029]
        log_A_site_II = [1.5095, 1.5981, 1.26836]
        n_site_II = [1.15232, 1.05915, 0.76748]

        if self.parameters['corrosion_site'] == 1:
            log_A_values = log_A_site_I
            n_values = n_site_I
        elif self.parameters['corrosion_site'] == 2:
            log_A_values = log_A_site_II
            n_values = n_site_II

        for i in range(len(distances) - 1):
            if distances[i] <= self.parameters['distance'] <= distances[i + 1]:
                log_A = log_A_values[i] + (log_A_values[i + 1] - log_A_values[i]) * \
                        (self.parameters['distance'] - distances[i]) / (distances[i + 1] - distances[i])
                n = n_values[i] + (n_values[i + 1] - n_values[i]) * \
                    (self.parameters['distance'] - distances[i]) / (distances[i + 1] - distances[i])
                A = np.exp(log_A)
                return A * time ** n, "Time [years]", "Mass loss [μm]"

        if self.parameters['distance'] == distances[0]:
            A, n = np.exp(log_A_values[0]), n_values[0]
        elif self.parameters['distance'] == distances[-1]:
            A, n = np.exp(log_A_values[-1]), n_values[-1]

        return A * time ** n, "Time [years]", "Mass loss [μm]"
