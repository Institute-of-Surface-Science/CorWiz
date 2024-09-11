import pandas as pd
import streamlit as st
import numpy as np
from typing import Dict, Tuple
from .corrosion_model import CorrosionModel

class Feliu1993Model(CorrosionModel):
    """
    A corrosion model based on the research by Feliu et al. (1993) which predicts atmospheric corrosion
    from meteorological and pollution parameters.

    Reference:
        Feliu, S., Morcillo, Manuel, and Feliu Jr, S.
        "The prediction of atmospheric corrosion from meteorological and pollution parameters—I. Annual corrosion."
        Corrosion Science, 34(3), 403-414 (1993). Elsevier.
    """

    DATA_FILE_PATH_2 = '../data/tables/feliu1993_table_2.csv'
    DATA_FILE_PATH_4 = '../data/tables/feliu1993_table_4.csv'

    def __init__(self, json_file_path: str):
        super().__init__(json_file_path=json_file_path, model_name='Feliu1993Model')
        self.parameters: Dict[str, float] = {}
        self.table_2, self.table_4 = self._load_data()

    def _load_data(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Loads the relevant data tables for the Feliu1993 model."""
        table_2 = pd.read_csv(self.DATA_FILE_PATH_2, header=None)
        table_4 = pd.read_csv(self.DATA_FILE_PATH_4, header=None)
        return table_2, table_4

    def display_parameters(self) -> None:
        """Displays the parameters selection interface for the user."""
        atmosphere_types = self.table_4.iloc[0, 1:].tolist()
        atmosphere_types.append("Enter Cl^- and SO_2 pollution annual averages")
        atmosphere = st.selectbox('Select Atmosphere:', atmosphere_types)

        self.parameters.update({
            'Binary Interaction': st.selectbox('Use Binary Interaction?', [True, False]),
            'Atmosphere': atmosphere_types.index(atmosphere),
            'Chloride pollution annual average': float(
                st.text_input(r"$Cl^-$ - Chloride pollution annual average  $[mg Cl^{-} dm^{-2} d^{-1}]$",
                              str(self.table_2.iloc[7, 2]))),
            'SO2 pollution annual average': float(
                st.text_input(r"$SO_2$ - SO2 pollution annual average  $[mg SO_2 dm^{-2} d^{-1}]$",
                              str(self.table_2.iloc[7, 2]))),
            'Temperature': float(st.text_input(r"$T$ - Temperature [°C]", str(self.table_2.iloc[6, 2]))),
            'Wetness time': float(st.text_input(r"$T_w$ - Wetness time [annual fraction]", str(self.table_2.iloc[4, 2])))
        })

        st.markdown(
            r"""
            **Annual corrosion, $A [\mu m]$:**
            - With Binary Interaction: $A = 132.4 \cdot Cl^- \cdot (1 + 0.038 \cdot T - 1.96 \cdot T_w - 0.53 \cdot SO_2 + 74.6 \cdot T_w \cdot (1 + 1.07 \cdot SO_2) - 6.3)$
            - Without Binary Interaction: $A = 33.0 + 57.4 \cdot Cl^- + 26.6 \cdot SO_2$

            **Exponent, $n$:**
            - $n = 0.570 + 0.0057 \cdot Cl^- \cdot T + 7.7 \times 10^{-4} \cdot D - 1.7 \times 10^{-3} \cdot A$
            """
        )

    def evaluate_material_loss(self, time: float) -> float:
        """Calculates and returns the material loss over time for the selected atmospheric condition."""
        # Calculate the annual corrosion
        if self.parameters['Binary Interaction']:
            annual_corrosion = (132.4 * self.parameters['Chloride pollution annual average'] *
                                (1 + 0.038 * self.parameters['Temperature'] -
                                 1.96 * self.parameters['Wetness time'] -
                                 0.53 * self.parameters['SO2 pollution annual average'] +
                                 74.6 * self.parameters['Wetness time'] *
                                 (1 + 1.07 * self.parameters['SO2 pollution annual average']) -
                                 6.3))
        else:
            annual_corrosion = (33.0 +
                                57.4 * self.parameters['Chloride pollution annual average'] +
                                26.6 * self.parameters['SO2 pollution annual average'])

        # Determine the exponent
        if self.parameters['Atmosphere'] == 0:
            exponent = float(self.table_4.iloc[1, 1])
        elif self.parameters['Atmosphere'] == 1:
            exponent = float(self.table_4.iloc[1, 2])
        elif self.parameters['Atmosphere'] == 2:
            exponent = float(self.table_4.iloc[1, 3])
        else:
            exponent = (0.570 +
                        0.0057 * self.parameters['Chloride pollution annual average'] * self.parameters['Temperature'] +
                        7.7e-4 * self.parameters['Wetness time'] * 365 -
                        1.7e-3 * annual_corrosion)

        # Calculate the material loss over time
        material_loss = annual_corrosion * np.power(time, exponent)
        return material_loss, "Time [years]", "Mass loss [μm]"
