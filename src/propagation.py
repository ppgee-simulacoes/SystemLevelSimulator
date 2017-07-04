# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 14:15:55 2017

@author: Calil
"""

from numpy import log10, sqrt

from support.enumeration import PropagationModel, OkumuraEnv

class Propagation(object):
    """
        Calculates propagation losses.
        
        Properties:
            model <PopagationModel>: type of propagation model 
                (generic, free space of okumura-hata/COST)
            pl_d0 <float>: reference loss
            d0 <float>: reference distance
            alpha <float>: power loss coefficient
            freq_mhz <float>: frequency in MHz
            freq_ghz <float>: frequency in GHz
            hte <float>: BS height
            hre <float>: MS height
            env <OkumuraEnv>: Okumura-Hata/COST environment
            shadow_flag <Bool>: shadowing indicator flag
            shadow_var <float>: shadowing variance
            rand_state <RandomState>: random number generator
            
        Constructor:
            Syntax: self = Results(param,rand_state)
            Inputs: param <Parameters>: simulation parameters
                    rand_state <RandomState>: random number generator
            
        Methods:
            propagate: 
                Calculates path loss for given distance
                Syntax: path_loss = self.propagate(dist)
                Inputs: dist <float>: distance [meters]
                Outputs: path_loss <float>: path loss [dB]
                
        Author: Calil Queiroz
                calil_queiroz@hotmail.com
                
        Version History:
            V. 0.1 (Jun 13 2017) - create class 
    """
    
    def __init__(self,param,rand_state):
        
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
        self.__shadow_flag = param.shadowing
        self.__shadow_var = param.shadowing_variance
        
        self.rand_state = rand_state
        
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
            
        return pl + self._shadowing()
    
    def _shadowing(self):
        if(self.__shadow_flag):
            return self.rand_state.normal(0,sqrt(self.__shadow_var),1)
        else:
            return 0.0
        
    def _generic(self,d):
        pl = self.__pl_d0 + 10*self.__alpha*log10(d/self.__d0)
        return pl
    
    def _free_space(self,d):
        pl = 20*log10(self.__freq_ghz) + 20*log10(d) + 92.44
        return pl
    
    def _okumura(self,d):
        if(self.__env == OkumuraEnv.LARGE_URBAN):
            if(self.__freq_mhz <= 300):
                a = 8.29*(log10(1.54*self.__hre)**2)-1.1
            else:
                a = 3.2*(log10(11.75*self.__hre)**2)-4.97
        else:
            a = (1.1*log10(self.__freq_mhz) - 0.7)*self.__hre - \
            (1.56*log10(self.__freq_mhz) - 0.8)
        
        if(self.__freq_mhz <= 1500):    
            l_urb = 69.55 + 26.6*log10(self.__freq_mhz) - \
            13.82*log10(self.__hte) - a - \
            (44.9 - 6.55*log10(self.__hte))*log10(d)
        elif(self.__freq_mhz <= 2000):
            l_urb = 46.3 + 33.9*log10(self.__freq_mhz) - 13.82*log10(self.__hte) -\
            a + (44.9 - 6.55*log10(self.__hte))*log10(d)
            if(self.__env == OkumuraEnv.LARGE_URBAN):
                l_urb = l_urb + 3
        
        if(self.__env == OkumuraEnv.SMALL_URBAN or self.__env == OkumuraEnv.LARGE_URBAN):
            return l_urb
        elif(self.__env == OkumuraEnv.SUBURBAN):
            return l_urb - 2*(log10(self.__freq_mhz/28))**2 - 5.4
        elif(self.__env == OkumuraEnv.RURAL):
            return l_urb - 4.78*log10(self.__freq_mhz)**2 - \
        18.33*log10(self.__freq_mhz) - 40.98
        
        raise NameError('No return on Okumura model!')
        
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
    
    @property
    def shadow_flag(self):
        return self.__shadow_flag
        