# -*- coding: utf-8 -*-
"""
Created on Mon May 22 14:56:23 2017

@author: Calil
"""

import numpy as np

class BaseStation(object):
    """
        Base station of mobile communications system.
        
        Properties:
            position <1x3 np.array>: xyz coordinates of BS position [meters]
            azimuth <1x1 float>: azimuth angle
            down_tilt <1x1 float>: mechanical antenna down tilt
            tx_power <1x1 float>: maximum transmit power
            ms_list <list>: list of connected mobile stations
            
        Constructor:
            Syntax: self = BaseStation(position,azimuth,tilt,power)
            Inputs: position <1x3 float>: xyz coordinates of BS position [meters]
                    azimuth <1x1 float>: azimuth angle
                    tilt <1x1 float>: mechanical antenna down tilt
                    power <1x1 float>: maximum transmit power
                    
        Methods:
            
                
        Author: Calil Queiroz
                calil_queiroz@hotmail.com
                
        Version History:
            V. 0.1 (May 22 2017) - create class
    """
    
    def __init__(self,position,azimuth,tilt,power):
        
        self.__position = position
        self.__tx_power = power
        self.__down_tilt = tilt
        self.__azimuth = azimuth
        
        self.__ms_list = []
        
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