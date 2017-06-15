# -*- coding: utf-8 -*-
"""
Created on Thu May 18 11:34:15 2017

@author: Calil
"""
import numpy as np
from support.enumeration import SimType, RandomSeeds, PropagationModel, OkumuraEnv


class Parameters(object):
    """
        Parameters class, which holds the simulation parameters.
        
        Properties:
            cell_radius <1x1 float>: radius of cell [meters]
            num_layers <1x1 int>: number of interference layers
            bs_height <1x1 float>: height of base stations [meters]
        
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
    
    ###########################################################################
    # SIMULATION PARAMETERS

    # Simulation Type (FIXED_SEEDS OR FIXED_CONF)
    simulation_type = SimType.FIXED_SEEDS

    # Maximum Number of Drops
    max_num_drops = 10

    # Set of seeds for Random States
    set_size = 100000
    seed_set = np.random.randint(1, 230522, set_size)
    state_indexes = [RandomSeeds.MOBILE_POSITION.value]

    # Simulation Seeds
    seeds = np.random.randint(1, set_size, max_num_drops)

    # Radius of cell [meters]
    cell_radius = 200
    
    # Number of interference layers
    num_layers = 2
    
    # Height of Base Stations [meters]
    bs_height = 40
    
    # Base Station azimuth angle [degrees]
    bs_azimuth = [60, 180, 300]
    
    # Base Station down tilt angle [degrees]
    bs_down_tilt = -10
    
    # Base Station transmit power [dBm]
    bs_power = 40
    
    # Base Station noise spectral density [dBm/Hz]
    bs_n0 = -150
    
    # Base Station transmit bandwidth [MHz]
    bs_band = 10
    
    # Total number of mobile stations
    num_ms = 50
    
    # Mobile station transmit power
    ms_tx_power = 20
    
    # Height of mobile stations
    ms_height = 1.5
    
    # Propagation model
    propagation_model = PropagationModel.GENERIC
    
    #General parameters
    # Frequency [MHz]
    frequency = 700
    
    # Generic model parameters
    # Reference loss [dB]
    ref_loss = 3
    
    # Reference distance [km]
    ref_distance = 1
    
    # Loss coefficiet
    loss_coef = 2.5
    
    # Okumura-Hata/COST parameters
    # Environment type
    okumura_env = OkumuraEnv.SMALL_URBAN
    
    # Shadowing flag
    shadowing = False
    
    # Shadowing variance [dB]
    shadowing_variance = 2