# -*- coding: utf-8 -*-
"""
Created on Thu May 25 17:19:54 2017

@author: Calil
"""

import unittest

from simulation_thread import SimulationThread
from parameters import Parameters

class SimulationThreadTest(unittest.TestCase):
    
    def setUp(self):
        self.param = Parameters(0)
        self.param.cell_radius = 200
        self.param.num_layers = 1
        self.param.bs_height = 10
        self.param.bs_azimuth = [60, 180, 300]
        self.param.bs_down_tilt = -10
        self.param.bs_power = 40
        
        self.sim_thread = SimulationThread(self.param)
        
    def test_bs_list(self):
        self.assertEqual(len(self.sim_thread.bs_list),7)
        
if __name__ == '__main__':
    unittest.main()