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
        print(parameters)
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
