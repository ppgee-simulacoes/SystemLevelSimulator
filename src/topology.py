# -*- coding: utf-8 -*-
"""
Created on Thu May 18 11:34:15 2017

@author: Calil
"""

import numpy as np

from base_station import BaseStation
from parameters import Parameters

class Topology(object):
    """
        Generates simulation topology, calculating the position of the BSs.
        
        Properties:
            radius <1x1 float>: cell radius [meters]
            num_layers <1x1 int>: number of interference layers
            bs_list <1xN list>: list of all BSs
            
        Constructor:
            Syntax: self = Topology(param)
            Inputs: param <Parameters>: simulation parameters
                    
        Methods:
            get_base_stations:
                Creates BS objects according to exagonal topology.
                Syntax: bs_list = self.get_base_stations()
                Outputs: bs_list <list>: list containing all the BS objects
                
        Author: Calil Queiroz
                calil_queiroz@hotmail.com
                
        Version History:
            V. 0.1 (May 18 2017) - create class skeleton 
    """
    
    def __init__(self,param):
        
        self.param = param
        
        self.__radius = param.cell_radius
        self.__num_layers = param.num_layers
        self.__bs_list = []
        
    @property
    def radius(self):
        return self.__radius
    
    @property
    def num_layers(self):
        return self.__num_layers
    
    @property
    def bs_list(self):
        return self.__bs_list
    
    def get_base_stations(self):
        pass