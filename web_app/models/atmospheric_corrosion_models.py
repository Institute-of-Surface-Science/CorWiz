import numpy as np
import pandas as pd


class atmospheric_corrosion_model:
    def __init__(self):
        self.article_identifier = 'parent class'


    def eval_material_loss(self):
        pass


    def get_model_name(self):
        return self.model_name


class i_the_prediction_of_atmospheric_corrosion_from_met(atmospheric_corrosion_model):
    '''
        @article{feliu1993prediction,
        title={I_The prediction of atmospheric corrosion from meteorological and pollution parameters—I. Annual corrosion},
        author={Feliu, S and Morcillo, Manuel and Feliu Jr, S},
        journal={Corrosion Science},
        volume={34},
        number={3},
        pages={403--414},
        year={1993},
        publisher={Elsevier}
    '''
    def __init__(self, binary_interaction, atmosphere, parameters):
        atmospheric_corrosion_model.__init__(self)
        self.model_name = 'The prediction of atmospheric corrosion from meteorological and pollution parameters—I. Annual corrosion'
        self.article_identifier = 'i_the_prediction_of_atmospheric_corrosion_from_met'
        self.binary_interaction = binary_interaction
        self.atmosphere = atmosphere
        self.steel = "Carbon Steel"
        self.p = parameters


    def eval_annual_corrosion(self):

        if self.binary_interaction:
            annual_corrosion = (132.4 * self.p['Cl'] * 
                        (1 + 0.038 * self.p['temp'] - 
                         1.96 * self.p['tw'] - 
                         0.53 * self.p['SO2'] + 
                         74.6 * self.p['tw'] * (1 + 1.07 * self.p['SO2']) - 
                         6.3))
        else:
            annual_corrosion = (33.0 + 
                        57.4 * self.p['Cl'] + 
                        26.6 * self.p['SO2'])

        return annual_corrosion
    

    def evaluate_exponent(self):
        table_4 = pd.read_csv('../data/tables/i_the_prediction_of_atmospheric_corrosion_from_met_tables_table_4.csv', header=None)
        if self.atmosphere == 0:
            exponent = table_4.iloc[1, 1]
        elif self.atmosphere == 1:
            exponent = table_4.iloc[1, 2]
        elif self.atmosphere == 2:
            exponent = table_4.iloc[1, 3]
        else:
            exponent = (0.570 + 
            0.0057 * self.p['Cl'] * self.p['temp'] + 
            7.7e-4 * self.p['D'] - 
            1.7e-3 * self.eval_annual_corrosion())

        return float(exponent)
    

    def eval_material_loss(self, time):

        material_loss = self.eval_annual_corrosion()*np.power(time, self.evaluate_exponent())
        return material_loss


class iso_9224(atmospheric_corrosion_model):
    
    '''

    '''
    def __init__(self, parameters):
        atmospheric_corrosion_model.__init__(self)
        self.model_name = 'ISO 9223:2012 and ISO 9224:2012'
        self.article_identifier = ['din-en-iso-92232012-05', 'din-en-iso-92242012-05']
        self.steel = "Unalloyed Steel"
        self.p = parameters
        self.correlation_speed_provided = 'corrosion_speed' in parameters

    
    def eval_corrosion_speed(self):

        if self.p['T'] <= 10:
            fst = 0.15*(self.p['T'] - 10)
        else:
            fst = -0.054*(self.p['T'] - 10)

        corrosion_speed = 1.77*self.p['Pd']**0.52*np.e**(0.02*self.p['RH'] + fst) + 0.102*self.p['Sd']**0.62*np.e**(0.033*self.p['RH'] + 0.04*self.p['T'])
        return corrosion_speed


    def eval_material_loss(self, time):
        
        if self.correlation_speed_provided:
            corrosion_speed = self.p['corrosion_speed']
        else:
            corrosion_speed = self.eval_corrosion_speed()
        
        if np.max(time) < 20:
            material_loss = self.p['exponent']*corrosion_speed*time**(self.p['exponent'] - 1)
        else:
            material_loss = corrosion_speed*(20**self.p['exponent'] + self.p['exponent']*20**(self.p['exponent'] - 1)*(time - 20))

        return material_loss
    

class tropical_marine_env(atmospheric_corrosion_model):
    '''
        @article{ma2010atmospheric,
        title={The atmospheric corrosion kinetics of low carbon steel in a tropical marine environment},
        author={Ma, Yuantai and Li, Ying and Wang, Fuhui},
        journal={Corrosion Science},
        volume={52},
        number={5},
        pages={1796--1800},
        year={2010},
        publisher={Elsevier}
        }
    '''

    def __init__(self, parameters):
        atmospheric_corrosion_model.__init__(self)
        self.model_name = 'The atmospheric corrosion kinetics of low carbon steel in a tropical marine environment'
        self.article_identifier = ['a_general_corrosion_function_in_terms_of_atmospher']
        self.steel = "Low Carbon Steel (Q235)"
        self.p = parameters

    
    def eval_corrosion_speed_and_exponent(self):
    # Define the distance points and their corresponding log(A) and n values
        distances = [25, 95, 375]
        
        # Site I values
        log_A_site_I = [0.13548, 0.52743, 0.44306]
        n_site_I = [2.86585, 2.18778, 1.55029]
        
        # Site II values
        log_A_site_II = [1.5095, 1.5981, 1.26836]
        n_site_II = [1.15232, 1.05915, 0.76748]
        
        # Select the site data
        if self.p['corrosion_site'] == 1:
            log_A_values = log_A_site_I
            n_values = n_site_I
        elif self.p['corrosion_site'] == 2:
            log_A_values = log_A_site_II
            n_values = n_site_II
        
        # Find the position for interpolation
        for i in range(len(distances) - 1):
            if distances[i] <= self.p['distance'] <= distances[i + 1]:
                # Linear interpolation for log(A)
                log_A = log_A_values[i] + (log_A_values[i + 1] - log_A_values[i]) * (self.p['distance'] - distances[i]) / (distances[i + 1] - distances[i])
                # Linear interpolation for n
                n = n_values[i] + (n_values[i + 1] - n_values[i]) * (self.p['distance'] - distances[i]) / (distances[i + 1] - distances[i])
                return np.exp(log_A), n
        
        # If the distance is exactly at one of the boundary points
        if self.p['distance'] == distances[0]:
            return np.exp(log_A_values[0]), n_values[0]
        elif self.p['distance'] == distances[-1]:
            return np.exp(log_A_values[-1]), n_values[-1]


    def eval_material_loss(self, time):

        A, n = self.eval_corrosion_speed_and_exponent()

        material_loss = A*time**n
        return material_loss
    

class a_general_corrosion_function(atmospheric_corrosion_model):
    '''
        @article{benarie1986general,
        title={A general corrosion function in terms of atmospheric pollutant concentrations and rain pH},
        author={Benarie, Michel and Lipfert, Frederick L},
        journal={Atmospheric Environment (1967)},
        volume={20},
        number={10},
        pages={1947--1958},
        year={1986},
        publisher={Elsevier}
        }

    '''

    def __init__(self, parameters):
        atmospheric_corrosion_model.__init__(self)
        self.model_name = 'A general corrosion function in terms of atmospheric pollutant concentrations and rain pH'
        self.article_identifier = ['a_general_corrosion_function_in_terms_of_atmospher']
        self.steel = "Carbon Steel"
        self.p = parameters

    
    def eval_corrosion_speed_and_exponent(self):
        table_2 = pd.read_csv('../data/tables/a_general_corrosion_function_in_terms_of_atmospher_tables_table_2.csv', header=None)
        A = float(table_2.iloc[self.p['corrosion_site'], 1])
        b = float(table_2.iloc[self.p['corrosion_site'], 2])

        return A, b 

    
    def eval_material_loss(self, time):
        A, n = self.eval_corrosion_speed_and_exponent()
        
        material_loss = A*time**n
        return material_loss
    

class coated_mass_loss_model(atmospheric_corrosion_model):
    '''
        @article{soares1999reliability,
        title={Reliability of maintained, corrosion protected plates subjected to non-linear corrosion and compressive loads},
        author={Soares, C Guedes and Garbatov, Yordan},
        journal={Marine structures},
        volume={12},
        number={6},
        pages={425--445},
        year={1999},
        publisher={Elsevier}
        }

    '''

    def __init__(self, parameters):
        atmospheric_corrosion_model.__init__(self)
        self.model_name = 'Reliability of maintained, corrosion protected plates subjected to non-linear corrosion and compressive loads'
        self.article_identifier = ['reliability_of_maintained_corrosion_protected_plat']
        self.steel = "Steel"
        self.p = parameters

    
    def eval_material_loss(self, time):
        
        material_loss = np.zeros_like(time)  # Initialize the material_loss array with zeros
        mask = time >= self.p['t_c']  # Create a boolean mask for time elements >= T_c
        material_loss[mask] = self.p['d_inf'] * (1 - np.exp(-(time[mask] - self.p['t_c']) / self.p['t_t']))
        return material_loss
    

class sophisticated_corrosion_rate(atmospheric_corrosion_model):
    '''
        @article{klinesmith2007effect,
        title={Effect of environmental conditions on corrosion rates},
        author={Klinesmith, Dawn E and McCuen, Richard H and Albrecht, Pedro},
        journal={Journal of Materials in Civil Engineering},
        volume={19},
        number={2},
        pages={121--129},
        year={2007},
        publisher={American Society of Civil Engineers}
}
    '''

    def __init__(self, parameters):
        atmospheric_corrosion_model.__init__(self)
        self.model_name = 'Effect of environmental conditions on corrosion rates'
        self.article_identifier = ['effect_of_environmental_conditions_on_corrosion_ra']
        self.steel = "Carbon Steel"
        self.p = parameters

    
    def eval_material_loss(self, time):
        
        table_2 = pd.read_csv('../data/tables/effect_of_environmental_conditions_on_corrosion_ra_tables_table_2.csv', header=None)
        A = float(table_2.iloc[1, 2])
        B = float(table_2.iloc[1, 3])
        C = float(table_2.iloc[1, 4])
        D = float(table_2.iloc[1, 5])
        E = float(table_2.iloc[1, 6])
        F = float(table_2.iloc[1, 7])
        G = float(table_2.iloc[1, 8])
        H = float(table_2.iloc[1, 9])
        J = float(table_2.iloc[1, 10])
        T0 = float(table_2.iloc[1, 11])

        material_loss = A*(time**B)*((self.p['TOW']*24/C)**D)*(1+(self.p['SO2']/E)**F)*(1+(self.p['Cl']/G)**H)*(np.exp(J*(self.p['T']+T0)))
        return material_loss

    


