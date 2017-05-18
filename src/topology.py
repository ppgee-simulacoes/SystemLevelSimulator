# -*- coding: utf-8 -*-
"""
Created on Thu May 18 11:34:15 2017

@author: Calil
"""

class Topology(object):
    """
        Generates simulation topology, calculating the position of the BSs.
        
        Properties:
            radius <1x1 float>: cell radius [meters]
            layers <1x1 int>: number of interference layers
            height <1x1 float>: height of base stations [meters]
            
        Constructor:
            Syntax: self = Topology(radius,layers,bs_height)
            Inputs: radius <1x1 float>: radius of cell [meters]
                    layers <1x1 int>: number of interference layers
                    bs_height <1x1 float>: height of base stations [meters]
                    
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
    
    def __init__(self,radius,layers,bs_height):
        pass
    
    def get_base_stations(self):
        pass