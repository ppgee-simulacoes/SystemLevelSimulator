# -*- coding: utf-8 -*-
"""
Created on Thu May 18 10:42:36 2017

@author: Calil
"""

class Parameters(object):
    
    __instance = None
    
        
    def __new__(cls):
        """
        This is the Singleton Pattern to ensure that this class will have only
        one instance
        """
        if Parameters.__instance is None:
            Parameters.__instance = object.__new__(cls)
        return Parameters.__instance
    
    #########################################################################
    # SIMULATION PARAMETERS