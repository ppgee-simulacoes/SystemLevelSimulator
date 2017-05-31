# -*- coding: utf-8 -*-
"""
Created on Mon May 22 17:03:40 2017

@author: Calil
"""

import numpy as np
import unittest
import numpy.testing as npt

from src.topology import Topology
from src.parameters.parameters import Parameters

class TopologyTest(unittest.TestCase):
    
    def setUp(self):
        self.param = Parameters()
        self.param.cell_radius = 200
        self.param.num_layers = 1
        self.param.bs_height = 10
        self.param.bs_azimuth = [60, 180, 300]
        self.param.bs_down_tilt = -10
        self.param.bs_power = 40
        
        # Topology with one layer
        self.topology_1 = Topology(self.param)
        
        # Topology with two layers
        self.param.num_layers = 2
        self.topology_2 = Topology(self.param)
        
        # Topology with three layers
        self.param.num_layers = 3
        self.topology_3 = Topology(self.param)
        
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
        npt.assert_equal(self.topology_1.x,np.array([]))
        
    def test_y(self):
        npt.assert_equal(self.topology_1.y,np.array([]))
        
    def test_set_base_stations(self):
        # Test 1
        bs_list = self.topology_1.set_base_stations()
        npt.assert_allclose(self.topology_1.x,np.array([-346.41, 0.00, 346.41, \
                                                        -173.21, 173.21, -173.21,\
                                                        173.21]),atol=1e-2)
        npt.assert_allclose(self.topology_1.y,np.array([0.0, 0.0, 0.0,\
                                                        300.0, 300.0, -300.0,\
                                                        -300.0]),atol=1e-2)
        self.assertEqual(len(bs_list),7)
        npt.assert_allclose(bs_list[0].position,np.array([-346.41, 0.0, 10.0]),\
                            atol=1e-2)
        npt.assert_allclose(bs_list[6].position,np.array([173.21, -300.0, 10.0]),\
                            atol=1e-2)
        
        # Test 2
        bs_list = self.topology_2.set_base_stations()
        npt.assert_allclose(self.topology_2.x,np.array([-692.82, -346.41, 0.0,\
                                                        346.41,  692.82,-519.62,\
                                                        -173.21,  173.21,  519.62,\
                                                        -519.62,-173.21,  173.21,\
                                                        519.62, -346.41,    0.0,\
                                                        346.41, -346.41,    0.0,\
                                                        346.41]),atol=1e-2)
        npt.assert_allclose(self.topology_2.y,np.array([0.0, 0.0, 0.0, 0.0, 0.0,\
                                                        300.0, 300.0, 300.0, 300.0,\
                                                        -300.0,-300.0,-300.0,-300.0,\
                                                        600.0, 600.0, 600.0,\
                                                        -600.0, -600.0, -600.0]),\
                                                        atol=1e-2)
        self.assertEqual(len(bs_list),19)
        npt.assert_allclose(bs_list[0].position,np.array([-692.82, 0.0, 10.0]),\
                            atol=1e-2)
        npt.assert_allclose(bs_list[18].position,np.array([346.41, -600.0, 10.0]),\
                            atol=1e-2)
        
    def test_plot_topology(self):
        self.topology_1.set_base_stations()
        self.topology_1.plot_topology()
        
        self.topology_2.set_base_stations()
        self.topology_2.plot_topology()
        
        self.topology_3.set_base_stations()
        self.topology_3.plot_topology()

if __name__ == '__main__':
    unittest.main()