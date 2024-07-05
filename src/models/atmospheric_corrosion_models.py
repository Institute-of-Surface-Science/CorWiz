import numpy as np


class atmospheric_corrosion_model:
    def __init__(self):
        self.model_name = 'parent class'


    def eval_corrosion_rate(self):
        pass


    def eval_material_loss(self):
        pass


    def get_model_name(self):
        return self.model_name


class A11_gabratov(atmospheric_corrosion_model):
    '''

    '''
    def __init__(self, temp):
        atmospheric_corrosion_model.__init__(self)
        self.model_name = 'Garbatov et al. 2011'
        self.temp = temp


    def eval_corrosion_rate(self):
        return 0.0014*self.temp + 0.0154
    

    def eval_material_loss(self, time):
        r_corr = self.eval_corrosion_rate()
        return r_corr*time

