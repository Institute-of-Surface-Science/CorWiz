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


class thermo_nutrient_variability_steel_corrosion_model(immersed_corrosion_model):
    '''
        @article{Kovalenko_2016, 
        title={Long-term immersion corrosion of steel subject to large annual variations in seawater temperature and nutrient concentration}, 
        volume={13}, 
        ISSN={1744-8980}, 
        url={http://dx.doi.org/10.1080/15732479.2016.1229797}, 
        DOI={10.1080/15732479.2016.1229797}, 
        number={8}, 
        journal={Structure and Infrastructure Engineering}, 
        publisher={Informa UK Limited}, 
        author={Kovalenko, Roman and Melchers, Robert E. and Chernov, Boris}, 
        year={2016}, 
        month=sep, 
        pages={978–987} }

    '''

    def __init__(self, parameters):
        immersed_corrosion_model.__init__(self)
        self.model_name = 'Long-term immersion corrosion of steel subject to large annual variations in seawater temperature and nutrient concentration'
        self.article_identifier = ['long-term_immersion_corrosion_of_steel_subject_to_']
        self.steel = "Mild steel"
        self.p = parameters

    
    def eval_material_loss(self, time):
        material_loss = self.p['c_s'] + time*self.p['r_s']
        return material_loss


