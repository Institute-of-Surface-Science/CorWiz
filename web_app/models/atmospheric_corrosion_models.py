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
        self.p = parameters  # [0 - Cl, 1 - SO2, 2 - T (temperature), 3 - Tw (wetness time (annual fraction)), 4 - D(number of rainy days), 5 - n(exponent)]


    def eval_annual_corrosion(self):

        if self.binary_interaction:
            annual_corrosion = 132.4*self.p[0]*(1 + 0.038*self.p[2] - 1.96*self.p[3] - 0.53*self.p[1] + 74.6*self.p[3]*(1 + 1.07*self.p[1]) - 6.3)
        else:
            annual_corrosion = 33.0 + 57.4*self.p[0] + 26.6*self.p[1]
        return annual_corrosion
    
    def evaluate_exponent(self):
        table_4 = pd.read_excel('../bin/temp/tables.xlsx', sheet_name='Table_4', header=None, engine='openpyxl')
        if self.atmosphere == 0:
            exponent = table_4.iloc[1, 1]
        elif self.atmosphere == 1:
            exponent = table_4.iloc[1, 2]
        elif self.atmosphere == 2:
            exponent = table_4.iloc[1, 3]
        else:
            exponent = 0.570 + 0.0057*self.p[0]*self.p[2] + 7.7e-4*self.p[4] - 1.7e-3*self.eval_annual_corrosion()

        return exponent
    
    def eval_material_loss(self, time):

        material_loss = self.eval_annual_corrosion()*time**self.evaluate_exponent()
        return material_loss


class iso_9223(atmospheric_corrosion_model):
    
    '''

    '''
    def __init__(self, parameters):
        atmospheric_corrosion_model.__init__(self)
        self.model_name = 'ISO 9223:2012 and ISO 9224:2012'
        self.article_identifier = ['din-en-iso-92232012-05', 'din-en-iso-92242012-05']
        self.steel = "Unalloyed Steel"
        self.p = parameters  # [0 - Pd, 1 - Sd, 2 - RH, 3 - fst, 4- temp, 5 - b]

    
    def eval_corrosion_speed(self):

        if self.p[4] <= 10:
            fst = 0.15*(self.p[4] - 10)
        else:
            fst = -0.054*(self.p[4] - 10)

        corrosion_speed = 1.77*self.p[0]**0.52*np.e**(0.02*self.p[2] + fst) + 0.102*self.p[1]**0.62*np.e**(0.033*self.p[2] + 0.04*self.p[4])
        return corrosion_speed


    def eval_material_loss(self, time):
        
        corrosion_speed = self.eval_corrosion_speed()
        
        if time < 20:
            material_loss = self.p[5]*corrosion_speed*time**(self.p[5] - 1)
        else:
            material_loss = corrosion_speed*(20**self.p[5] + self.p[5]*20**(self.p[5] - 1)*(time - 20))

        return material_loss
