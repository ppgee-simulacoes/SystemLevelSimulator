# -*- coding: utf-8 -*-
"""
Created on Mon May 22 14:56:23 2017

@author: Calil
"""

from numpy import log10

class BaseStation(object):
    """
        Base station of mobile communications system.
        
        Properties:
            idx <1x1 int>: base station index
            position <1x3 np.array>: xyz coordinates of BS position [meters]
            azimuth <1x1 float>: azimuth angle
            down_tilt <1x1 float>: mechanical antenna down tilt
            tx_power <1x1 float>: maximum transmit power
            ms_list <list>: list of connected mobile stations
            
        Constructor:
            Syntax: self = BaseStation(position,azimuth,tilt,power,idx)
            Inputs: position <1x3 float>: xyz coordinates of BS position [meters]
                    azimuth <1x1 float>: azimuth angle
                    tilt <1x1 float>: mechanical antenna down tilt
                    power <1x1 float>: maximum transmit power
                    idx <1x1 inf>: base station index
                    
        Methods:
            
                
        Author: Calil Queiroz
                calil_queiroz@hotmail.com
                
        Version History:
            V. 0.1 (May 22 2017) - create class
    """

    def __init__(self,param,position,azimuth,num):
        
        self.__idx = num
        self.__position = position
        self.__tx_power = param.bs_power
        self.__down_tilt = param.bs_down_tilt
        lin_n0 = 10**(param.bs_n0/10)
        self.__noise = 10*log10(param.bs_band*1e6*lin_n0)
        self.__azimuth = azimuth
        
        self.__ms_list = []
        
    def connect_to(self,ms):
        self.__ms_list.append(ms)
        
    @property
    def position(self):
        return self.__position
    
    @property
    def tx_power(self):
        return self.__tx_power
    
    @property
    def down_tilt(self):
        return self.__down_tilt
    
    @property
    def azimuth(self):
        return self.__azimuth
    
    @property
    def ms_list(self):
        return self.__ms_list
    
    @property
    def idx(self):
        return self.__idx
    
    @property
    def noise(self):
        return self.__noise