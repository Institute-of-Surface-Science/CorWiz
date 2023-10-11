import numpy as np


class immersed_corrosion_model:
    def __init__(self):
        self.model_name = 'parent class'


    def eval_corrosion_rate(self):
        pass


    def eval_material_loss(self):
        pass


    def get_model_name(self):
        return self.model_name


class A11_gabratov(immersed_corrosion_model):
    '''
    @article{garbatov2011corrosion,
    title={Corrosion modeling in marine structures},
    author={Garbatov, Y and Zayed, A and Soares, C Guedes},
    journal={Marine Technology and Engineering. London, UK: Taylor \& Francis Group},
    pages={1121--56},
    year={2011}
    }
    '''
    def __init__(self, temp):
        immersed_corrosion_model.__init__(self)
        self.model_name = 'Garbatov et al. 2011'
        self.temp = temp


    def eval_corrosion_rate(self):
        return 0.0014*self.temp + 0.0154
    

    def eval_material_loss(self, time):
        r_corr = self.eval_corrosion_rate()
        return r_corr*time


class A13_gabratov(immersed_corrosion_model):
    '''
    @article{garbatov2011corrosion,
    title={Corrosion modeling in marine structures},
    author={Garbatov, Y and Zayed, A and Soares, C Guedes},
    journal={Marine Technology and Engineering. London, UK: Taylor \& Francis Group},
    pages={1121--56},
    year={2011}
    }
    '''
    def __init__(self, temp, vf):
        immersed_corrosion_model.__init__(self)
        self.model_name = 'Gavaratov et al. 2011'
        self.temp = temp
        self.vf = vf


    def eval_corrosion_rate(self):
        return 0.9338*(1 - np.exp(-0.4457*(self.vf - 0.2817)))
    

    def eval_material_loss(self, time):
        r_corr = self.eval_corrosion_rate()
        return r_corr*time


class A15_pedeferri(immersed_corrosion_model):
    '''
    @book{pedeferri2018corrosion,
    title={Corrosion science and engineering},
    author={Pedeferri, Pietro and Ormellese, Marco},
    volume={720},
    year={2018},
    publisher={Springer}
    }
    '''
    def __init__(self, temp, vf, O2):
        immersed_corrosion_model.__init__(self)
        self.model_name = 'Pedeferri 2018'
        self.temp = temp
        self.vf = vf
        self.O2 = O2


    def eval_corrosion_rate(self):
        return 10*(2**((self.Tw - 25)/25))*(self.Ox + 0.04*self.Cl)*(1 + self.vf**0.5)
    

    def eval_material_loss(self, time):
        r_corr = self.eval_corrosion_rate()
        return r_corr*time


class A16_melchers_ahammed(immersed_corrosion_model):
    '''
    @article{melchers2006statistical,
    title={Statistical characterization of corroded steel plate surfaces},
    author={Melchers, RE and Ahammed, M},
    journal={Advances in Structural Engineering},
    volume={9},
    number={1},
    pages={83--90},
    year={2006},
    publisher={SAGE Publications Sage UK: London, England}
    }
    '''
    def __init__(self, temp, vf, O2, O2B):
        immersed_corrosion_model.__init__(self)
        self.model_name = 'Melchers and Ahammed (2006)'
        self.temp = temp
        self.vf = vf
        self.O2 = O2
        self.O2B = O2B


    def eval_corrosion_rate(self):
        return 0.056*np.exp(0.065*self.temp)*self.O2/self.O2B*(1 + 4.6*self.vf)
    

    def eval_material_loss(self, time):
        r_corr = self.eval_corrosion_rate()
        return r_corr*time


class A17_khodabux(immersed_corrosion_model):
    '''
    @article{khodabux2020profiling,
    title={Profiling corrosion rates for offshore wind turbines with depth in the North Sea},
    author={Khodabux, Waseem and Causon, Paul and Brennan, Feargal},
    journal={Energies},
    volume={13},
    number={10},
    pages={2518},
    year={2020},
    publisher={MDPI}
    }
    '''
    def __init__(self, HR):
        immersed_corrosion_model.__init__(self)
        self.model_name = 'Khodabux et al. (2020)'
        self.HR = HR


    def eval_corrosion_rate(self):
        return 1.075*self.HR**2 - 1.213*self.HR + 0.928
    

    def eval_material_loss(self, time):
        r_corr = self.eval_corrosion_rate()
        return r_corr*time


class A20_hicks_oster(immersed_corrosion_model):
    '''
    @article{hicks2012developing,
    title={Developing a risk assessment tool to predict the risk of accelerated corrosion to port infrastructure},
    author={Hicks, Randall E and Oster, Ryan J},
    journal={Great Lakes Maritime Research Institute},
    pages={1--20},
    year={2012}
    }
    '''
    def __init__(self, AK, SRB, Cs):
        immersed_corrosion_model.__init__(self)
        self.model_name = 'Hicks and Oster (2012)'
        self.AK = AK
        self.SRB = SRB
        self.Cs = Cs



    def eval_corrosion_rate(self):
        return (0.0021*self.AK + (0.015*np.log(self.SRB) + 0.0014*self.Cs)) - 0.0084
    

    def eval_material_loss(self, time):
        r_corr = self.eval_corrosion_rate()
        return r_corr*time