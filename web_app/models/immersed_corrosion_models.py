import numpy as np


class immersed_corrosion_model:
    def __init__(self):
        self.article_identifier = 'parent class'


    def eval_material_loss(self):
        pass


    def get_model_name(self):
        return self.model_name
    

class empirical_prediction_model(immersed_corrosion_model):
    '''
         @article{Ali_2020, title={The empirical prediction of weight change and corrosion rate of low-carbon steel}, 
         volume={6}, 
         ISSN={2405-8440}, 
         url={http://dx.doi.org/10.1016/j.heliyon.2020.e05050}, 
         DOI={10.1016/j.heliyon.2020.e05050}, 
         number={9}, 
         journal={Heliyon}, 
         publisher={Elsevier BV}, 
         author={Ali, Nurdin and Fulazzaky, Mohamad Ali}, 
         year={2020}, 
         month=sep, 
         pages={e05050} }

    '''

    def __init__(self, parameters):
        immersed_corrosion_model.__init__(self)
        self.model_name = 'The empirical prediction of weight change and corrosion rate of low-carbon steel'
        self.article_identifier = ['the_empirical_prediction_of_weight_change_and_corr']
        self.steel = "Low carbon steel"
        self.p = parameters

    
    def eval_material_loss(self, time):
        material_loss = (0.00006*self.p['C'] + 0.0008)*time + self.p['b']

        return material_loss
