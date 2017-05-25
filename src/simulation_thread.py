# -*- coding: utf-8 -*-
"""
Created on Thu May 18 11:04:05 2017

@author: Calil
"""

from topology import Topology

class SimulationThread(object):
    """
        Performs simulation thread, with multiple drops.
        
        Properties:
            param <Parameters>: simulation parameters
            topology <Topology>: network toloplogy and BS positions
            bs_list <list>: list of all the BS objects
            ms_list <list>: list of all MS objects
            
        Constructor:
            Syntax: self = SimulationThread(param)
            Inputs: param <Parameters>: simulation parameters
            
        Methods:
            create_ms:
                Uses topology to create MS objects and save them in ms_list
                property.
                
        Author: Calil Queiroz
                calil_queiroz@hotmail.com
                
        Version History:
            V. 0.1 (May 18 2017) - create class skeleton  
    """
    
    def __init__(self,param):
        
        self.topology = Topology(param)
        self.bs_list = self.topology.set_base_stations()
    
    def create_ms(self):
        pass
    