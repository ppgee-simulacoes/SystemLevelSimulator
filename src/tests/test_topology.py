# -*- coding: utf-8 -*-
"""
Created on Mon May 22 17:03:40 2017

@author: Calil
"""

import numpy as np
import unittest
import numpy.testing as npt

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
        
    def test_r(self):
        self.assertEqual(self.topology_1.r,200)
        
    def test_num_layers(self):
        self.assertEqual(self.topology_1.num_layers,1)
        
    def test_bs_list(self):
        self.assertEqual(len(self.topology_1.bs_list),0)
        
    def test_h(self):
        self.assertAlmostEqual(self.topology_1.h,173.205,delta=1e-3)
        
    def test_num_rows(self):
        self.assertEqual(self.topology_1.num_rows,3)
        
    def test_max_hex(self):
        self.assertEqual(self.topology_1.max_hex,3)
        
    def test_bot_row(self):
        self.assertEqual(self.topology_1.bot_row,2)
        
    def test_num_bs(self):
        self.assertEqual(self.topology_1.num_bs,7)
        
    def test_x(self):
        npt.assert_equal(self.topology_1.x,np.zeros(7))
        
    def test_y(self):
        npt.assert_equal(self.topology_1.y,np.zeros(7))

if __name__ == '__main__':
    unittest.main()