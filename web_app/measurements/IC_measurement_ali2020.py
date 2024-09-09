import pandas as pd
import streamlit as st
import numpy as np
from typing import Dict, Optional
from .corrosion_measurement import CorrosionMeasurement
from typing import Tuple, Optional
from scipy.interpolate import interp2d, RegularGridInterpolator

class Ali2020Measurement(CorrosionMeasurement):
    """
    A corrosion measurement based on the study by Ali and Fulazzaky (2020) which predicts the weight change
    and corrosion rate of low-carbon steel.

    Reference:
        Ali, Nurdin, and Mohamad Ali Fulazzaky.
        "The empirical prediction of weight change and corrosion rate of low-carbon steel."
        Heliyon, 6(9), e05050 (2020). Elsevier.
    """

    DATA_FILE_PATHS = {'table_4': '../data/tables/ali2020_table_4.csv',
    }

    def __init__(self, json_file_path: str):
        super().__init__(json_file_path=json_file_path, measurement_name='Ali2020Measurement')
        self.table_4 = self._load_data()
        self.parameters: Dict[str, float] = {}

    def _load_data(self) -> pd.DataFrame:
        """Loads the relevant data tables for the Ali2020 measurement."""
        return (
            pd.read_csv(self.DATA_FILE_PATHS['table_4'], header=None)
        )

    def display_parameters(self) -> None:
        """Prompts the user to input values for all parameters and returns a dictionary of the parameters."""

        # Load the data and calculate 'b'
        nacl_concs = (self.table_4.iloc[1, 1:].astype(float)).to_list()

        nacl_conc = st.selectbox('Select NaCl concentraion [$\%w/w$]:', nacl_concs)
        nacl_conc_index = nacl_concs.index(nacl_conc)

        self.parameters['C'] = nacl_conc_index

    def get_material_loss(self) -> np.ndarray:
        """
        Return the material loss over time based on the selected parameters.

        Returns:
            np.ndarray: The material loss (T vs Material loss).
        """
        
        time = self.table_4.iloc[2:,0]
        material_loss = self.table_4.iloc[2:, self.parameters['C']+1]

        material_loss = np.column_stack((time.to_numpy(), material_loss.to_numpy()))

        return material_loss

