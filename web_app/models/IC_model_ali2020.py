import pandas as pd
import streamlit as st
import numpy as np
from typing import Dict, Optional
from .corrosion_model import CorrosionModel
from typing import Tuple, Optional
from scipy.interpolate import interp2d, RegularGridInterpolator

class Ali2010Model(CorrosionModel):
    """
    A corrosion model based on the study by Ali and Fulazzaky (2020) which predicts the weight change
    and corrosion rate of low-carbon steel.

    Reference:
        Ali, Nurdin, and Mohamad Ali Fulazzaky.
        "The empirical prediction of weight change and corrosion rate of low-carbon steel."
        Heliyon, 6(9), e05050 (2020). Elsevier.
    """

    DATA_FILE_PATHS = {'table_3': '../data/tables/ali2020_tables_table_3.csv',
                      'table_4': '../data/tables/ali2020_tables_table_4.csv'
    }

    def __init__(self, parameters: Optional[Dict[str, float]] = None):
        super().__init__(model_name='Empirical Prediction of Weight Change and Corrosion Rate of Low-Carbon Steel')
        self.table_3, self.table_4 = self._load_data()
        self.parameters = parameters if parameters else self._get_parameters()

    def _load_data(self) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Loads the relevant data tables for the ISO 9224 model."""
        return (
            pd.read_csv(self.DATA_FILE_PATHS['table_3'], header=None),
            pd.read_csv(self.DATA_FILE_PATHS['table_4'], header=None),
        )


    def _get_parameters(self) -> Dict[str, float]:
        """Prompts the user to input values for all parameters and returns a dictionary of the parameters."""
        limits = {
            'C': {'desc': 'Concentration of NaCl', 'lower': 0.0, 'upper': 5.0, 'unit': '%w/w'},
        }

        parameters = {}
        for symbol, limit in limits.items():
            value = st.number_input(
                f"${symbol}$ - Enter {limit['desc']} [${limit['unit']}$]:",
                min_value=float(limit['lower']),
                max_value=float(limit['upper']),
                value=float(limit['lower']),
                step=0.01,
                key=f"input_{symbol}"
            )
            parameters[symbol] = value

        # Load the data and calculate 'b'
        nacl_concs = np.array(self.table_3.iloc[1:, 0].astype(float))
        constants = np.array(self.table_3.iloc[1:, 2].astype(float))

        # Interpolate or get the exact 'b' value
        if parameters['C'] in nacl_concs:
            parameters['b'] = constants[nacl_concs == parameters['C']][0]
        else:
            parameters['b'] = np.interp(parameters['C'], nacl_concs, constants)

        st.write(r'Mass loss due to corrosion, $W_L [\mu m] = (0.00006C + 0.0008)t + b $')

        return parameters

    def eval_material_loss(self, time: float) -> float:
        """
        Evaluates the material loss over time based on the provided parameters.

        Args:
            time (float): The time duration in years.

        Returns:
            float: The calculated material loss.
        """
        material_loss = (0.00006 * self.parameters['C'] + 0.0008) * time*24*365 + self.parameters['b']
        
        return material_loss

    def _bilinear_interpolation(self, x, y, values, nacl_concentration, time):
        """Perform bilinear interpolation."""
        x1 = np.searchsorted(nacl_concentration, x) - 1
        x2 = x1 + 1
        y1 = np.searchsorted(time, y) - 1
        y2 = y1 + 1
        
        x1 = np.clip(x1, 0, len(nacl_concentration) - 2)
        x2 = np.clip(x2, 1, len(nacl_concentration) - 1)
        y1 = np.clip(y1, 0, len(time) - 2)
        y2 = np.clip(y2, 1, len(time) - 1)
        
        x1_val = nacl_concentration[x1]
        x2_val = nacl_concentration[x2]
        y1_val = time[y1]
        y2_val = time[y2]
        
        Q11 = values[y1, x1]
        Q21 = values[y1, x2]
        Q12 = values[y2, x1]
        Q22 = values[y2, x2]
        
        return (Q11 * (x2_val - x) * (y2_val - y) +
                Q21 * (x - x1_val) * (y2_val - y) +
                Q12 * (x2_val - x) * (y - y1_val) +
                Q22 * (x - x1_val) * (y - y1_val)) / ((x2_val - x1_val) * (y2_val - y1_val))


    def eval_material_loss_exp(self, time:float) -> float:
        """Evaluates the material loss over time based on the experimental data.
        
        Args:
            time (float): The time duration in years.
            
        Returns:
            float: The calculated material loss.
        """
    
        return self._bilinear_interpolation(self.parameters['C'], 
                                       time, 
                                       self.table_4.iloc[2:, 1:].astype(float).to_numpy(), 
                                       self.table_4.iloc[1, 1:].astype(float).to_numpy(), 
                                       self.table_4.iloc[2:, 0].astype(float).to_numpy() / 24 / 365)

