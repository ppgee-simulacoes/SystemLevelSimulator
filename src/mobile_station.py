# -*- coding: utf-8 -*-
"""
Created on Thu May 25 16:47:46 2017

@author: Calil
"""

import numpy as np

from base_station import BaseStation

class MobileStation(object):
    """
        Mobile station of mobile communications system.
        
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
            V. 0.1 (May 25 2017) - create class
    """
    
    def __init__(self,position,power,num):
        
        self.__idx = num
        
        self.__position = position
        self.__tx_power = power
        
        self.__connected_to = None
        
    @property
    def position(self):
        return self.__position
    
    @property
    def tx_power(self):
        return self.__tx_power
    
    @property
    def idx(self):
        return self.__idx
    
    @property
    def connected_to(self):
        return self.__connected_to
    
    @connected_to.setter
    def connected_to(self,bs):
        self.__connected_to = bs