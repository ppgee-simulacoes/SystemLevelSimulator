# -*- coding: utf-8 -*-
"""
Created on Thu May 18 11:34:15 2017

@author: Calil
"""
import numpy as np
from support.enumeration import SimType, RandomSeeds, PropagationModel, PropagationEnvironment


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
        # This is the Singleton Pattern to ensure that this class will have only
        # one instance

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
    state_indexes = [RandomSeeds.MOBILE_POSITION.value, RandomSeeds.SHADOWING.value, RandomSeeds.ACTIVE_MOBILE.value]

    # Simulation Seeds
    seeds = np.random.randint(1, set_size, max_num_drops)

    # TOPOLOGY PARAMETERS
    # Radius of cell [meters]
    cell_radius = 200
    
    # Number of interference layers
    num_layers = 2

    # Plot grid for each drop
    plot_drop_grid = False

    # BASE STATION PARAMETERS
    # Height of Base Stations [meters] (between 30 and 200m)
    bs_height = 40
    
    # Base Station azimuth angle [degrees]
    bs_azimuth = [30, 150, 270]
    
    # Base Station down tilt angle [degrees]
    bs_down_tilt = -5
    
    # Base Station transmit power [dBm]
    bs_power = 40

    # MS Noise spectral density [dBm/Hz]
    bs_n0 = -200

    # MS Transmit Bandwidth [Hz]
    bs_bandwidth = 5e6

    # MOBILE STATION PARAMETERS
    # Total number of mobile stations
    num_ms = 500
    
    # Mobile station transmit power [dBm]
    ms_power = 20
    
    # Height of mobile stations [meters] (between 1 and 10m)
    ms_height = 1.5

    # MS Noise spectral density [dBm/Hz]
    ms_n0 = -90

    # MS Transmit Bandwidth [Hz]
    ms_bandwidth = 10e6

    # PROPAGATION PARAMETERS
    # Propagation Model (GENERIC, FREE_SPACE, OKUMURA_COST)
    propagation_model = PropagationModel.GENERIC
    if propagation_model == PropagationModel.OKUMURA_COST:
        propagation_environment = PropagationEnvironment.URBAN

    # Path Loss Log-normal exponent (usually between 2 and 4)
    pl_alpha = 2

    # Distance of reference [meters]
    d0 = 100

    # Path Loss for distance of reference [dB]
    pl_d0 = 30

    # Shadowing flag
    shadowing = True
    if shadowing is True:
        # Standard Deviation for Gaussian Variable [dB] (usually between 4 and 13 dB)
        pl_sigma = 3

    # Transmission Frequency [Hz]
    frequency = 300e6




