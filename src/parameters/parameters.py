# -*- coding: utf-8 -*-
"""
Created on Thu May 18 11:34:15 2017

@author: Calil
"""

class Parameters(object):
    """
        Parameters class, which holds the simulation parameters.
        
        Properties:
            
        
        Constructor:
            Syntax: self = Parameters()
            
        Author: Calil Queiroz
                calil_queiroz@hotmail.com
                
        Version History:
            V. 0.1 (May 18 2017) - create class skeleton
    """
    
    __instance = None
        
    def __new__(cls):

        #This is the Singleton Pattern to ensure that this class will have only
        #one instance

        if Parameters.__instance is None:
            Parameters.__instance = object.__new__(cls)
        return Parameters.__instance
    
    #########################################################################
    # SIMULATION PARAMETERS