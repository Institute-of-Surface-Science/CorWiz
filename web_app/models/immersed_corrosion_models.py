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


class immersion_corrosion_predictive_model_incorporating(immersed_corrosion_model):
    '''
        @article{garbatov2011corrosion,
        title={Corrosion modeling in marine structures},
        author={Garbatov, Y and Zayed, A and Soares, C Guedes},
        journal={Marine Technology and Engineering},
        year={2011}
        }
    '''

    def __init__(self, parameters):
        immersed_corrosion_model.__init__(self)
        self.model_name = 'Corrosion modeling in marine structures'
        self.article_identifier = ['corrosion_modeling_in_marine_structures']
        self.steel = "Mild carbon steel"
        self.p = parameters

    
    def eval_material_loss(self, time):
        
        d_Temperature = 0.0014*self.p['Temperature'] + 0.0154
        f_Temperature = self.p['Temperature']/15.5

        d_Dissolved_Oxygen = 0.0268*self.p['Dissolved Oxygen Concentration'] + 0.0086
        f_Dissolved_Oxygen = 0.9483*self.p['Dissolved Oxygen Concentration'] + 0.0517

        d_Flow_Velocity = 0.9338*(1 - np.exp(-0.4457*(self.p['Flow Velocity'] + 0.2817)))
        f_Flow_Velocity = 1.0978*(1 - np.exp(-2.2927*(self.p['Flow Velocity'] + 0.0548)))

        self.p['Nominal Corrosion Rate'] = d_Temperature + d_Dissolved_Oxygen + d_Flow_Velocity

        corrosion_rate = f_Temperature*f_Dissolved_Oxygen*f_Flow_Velocity*self.p['Nominal Corrosion Rate']

        material_loss = corrosion_rate*time

        return material_loss


