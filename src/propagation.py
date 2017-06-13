# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 14:15:55 2017

@author: Calil
"""

import numpy as np

from support.enumeration import PropagationModel, OkumuraEnv

class Propagation(object):
    
    def __init__(self,param):
        
        self.__model = param.propagation_model
        
        # Generic model parameters
        self.__pl_d0 = param.ref_loss
        self.__d0 = param.ref_distance
        self.__alpha = param.loss_coef
        
        # Free space parameters
        self.__freq_mhz = param.frequency
        self.__freq_ghz = self.__freq_mhz/1000
        
        # Okumura-Hata/COST parameters
        self.__hte = param.bs_height
        self.__hre = param.ms_height
        self.__env = param.okumura_env
        
        # Shadowing parameters
        self.__shadow_var = param.shadowing_variance
        
    def propagate(self,dist):
        
        # Convert distance to Kilometers
        d = dist/1000
        
        if(self.__model == PropagationModel.GENERIC):
            pl = self._generic(d)
        elif(self.__model == PropagationModel.FREESPACE):
            pl = self._free_space(d)
        elif(self.__model == PropagationModel.OKUMURA):
            pl = self._okumura(d)
        else:
            raise NameError('Unknown propagation model!')
            
        return pl
        
    def _generic(self,d):
        pl = self.__pl_d0 + 10*self.__alpha*np.log10(d/self.__d0)
        return pl
    
    def _free_space(self,d):
        pl = 20*np.log10(self.__freq_ghz) + 20*np.log10(d) + 92.44
        return pl
    
    def _okumura(self,d):
        pass
        
    @property
    def model(self):
        return self.__model
    
    @property
    def pl_d0(self):
        return self.__pl_d0
    
    @property
    def d0(self):
        return self.__d0
    
    @property
    def alpha(self):
        return self.__alpha
    
    @property
    def freq_mhz(self):
        return self.__freq_mhz
    
    @property
    def freq_ghz(self):
        return self.__freq_ghz
    
    @property
    def hte(self):
        return self.__hte
    
    @property
    def hre(self):
        return self.__hre
    
    @property
    def env(self):
        return self.__env
    
    @property
    def shadow_var(self):
        return self.__shadow_var
        