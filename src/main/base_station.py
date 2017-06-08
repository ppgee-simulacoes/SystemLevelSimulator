# -*- coding: utf-8 -*-
"""
Created on Thu May 24 21:56:15 2017
@author: Guilherme
"""

class BaseStation(object):
    """
    Generates simulation topology, calculating the position of the BSs.

    Properties:
        radius <1x1 float>: cell radius [meters]
        layers <1x1 int>: number of interference layers
        bs_height <1x1 float>: height of base stations [meters]

    Constructor:
        Syntax: self = Topology(radius,layers,bs_height)
        Inputs: radius <1x1 float>: radius of cell [meters]
                layers <1x1 int>: number of interference layers
                bs_height <1x1 float>: height of base stations [meters]

    Methods:
        get_base_stations:
            Creates BS objects according to hexagonal topology.
            Syntax: bs_list = self.get_base_stations()
            Outputs: bs_list <list>: list containing all the BS objects

    Author: Guilherme Oliveira

    Version History:
        V. 0.1 (May 24 2017) - create class BaseStation 
"""


    def __init__(self, x_position, y_position, z_position, bs_parameters):
        self.x_position = x_position
        self.y_position = y_position
        self.z_position = z_position
        self.tilt_angle = bs_parameters.tilt_angle
        self.azymuth_angle = bs_parameters.azymuth_angle
        self.transmission_power = bs_parameters.transmission_power
        self.mobile_station_list = []
        self.height = bs_parameters.height


    def get_base_stations(self):
        pass