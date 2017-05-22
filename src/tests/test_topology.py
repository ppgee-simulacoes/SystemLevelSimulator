# -*- coding: utf-8 -*-
"""
Created on Mon May 22 17:03:40 2017

@author: Calil
"""

import unittest

from topology import Topology
from parameters import Parameters

class TopologyTest(unittest.TestCase):
    
    def setUp(self):
        self.param = Parameters(0)
        self.param.cell_radius = 200
        self.param.num_layers = 1
        self.param.bs_height = 10
        self.param.bs_azimuth = [60, 180, 300]
        self.param.bs_down_tilt = -10
        self.param.bs_power = 40
        
        self.topology_1 = Topology(self.param)
        
    def test_radius(self):
        self.assertEqual(self.topology_1.radius,200)
        
    def test_num_layers(self):
        self.assertEqual(self.topology_1.num_layers,1)
        
    def test_bs_list(self):
        self.assertEqual(len(self.topology_1.bs_list),0)

if __name__ == '__main__':
    unittest.main()