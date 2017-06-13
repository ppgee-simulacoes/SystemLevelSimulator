# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 14:15:55 2017

@author: Calil
"""

class Propagation(object):
    
    def __init__(self,param):
        
        self.__model = param.propagation_model
        
        # Generic model parameters
        self.__pl_d0 = param.ref_loss
        self.__d0 = param.ref_distance
        self.__alpha = param.loss_coef
        
        # Free space parameters
        self.__freq = param.frequency
        
        # Okumura-Hata/COST parameters
        self.__hte = param.bs_height
        self.__hre = param.ms_height
        self.__env = param.okumura_env
        
        # Shadowing parameters
        self.__shadow_var = param.shadowing_variance
        
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
    def freq(self):
        return self.__freq
    
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
        