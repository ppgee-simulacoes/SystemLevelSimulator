# -*- coding: utf-8 -*-
"""
Created on Thu May 25 17:19:54 2017

@author: Calil
"""

import unittest
import matplotlib.pyplot as plt

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
        self.param.num_ms = 50
        self.param.ms_height = 1.5
        self.param.ms_tx_power = 20
        self.param.seeds = [983]
        
        self.sim_thread = SimulationThread(self.param)
        
        self.param.num_ms = 2
        self.param.num_layers = 0
        self.sim_thread_2 = SimulationThread(self.param)
        
        self.param.num_ms = 200
        self.param.num_layers = 2
        self.sim_thread_3 = SimulationThread(self.param)
        
    def test_num_ms(self):
        self.assertEqual(self.sim_thread.num_ms,50)
        self.assertEqual(self.sim_thread_2.num_ms,2)
        
    def test_bs_list(self):
        self.assertEqual(len(self.sim_thread.bs_list),7)
        
    def test_ms_list(self):
        self.assertEqual(len(self.sim_thread.ms_list),0)
        
    def test_current_seed(self):
        self.assertEqual(self.sim_thread.current_seed,983)
        
    def test_create_ms(self):
        self.sim_thread.create_ms()
        self.assertEqual(len(self.sim_thread.ms_list),50)
        self.assertEqual(len(self.sim_thread.x_ms),50)
        self.assertEqual(len(self.sim_thread.y_ms),50)
        
        self.sim_thread_2.create_ms()
        self.assertEqual(len(self.sim_thread_2.ms_list),2)
        self.assertEqual(len(self.sim_thread_2.x_ms),2)
        self.assertEqual(len(self.sim_thread_2.y_ms),2)
        
    def test_plot_grid(self):
        self.sim_thread.create_ms()
        ax = self.sim_thread.plot_grid()
        plt.show(ax)
        
        self.sim_thread_3.create_ms()
        ax = self.sim_thread_3.plot_grid()
        plt.show(ax)
        
if __name__ == '__main__':
    unittest.main()
    
#    suite = unittest.TestSuite()
#    suite.addTest(SimulationThreadTest("test_plot_grid"))
#    runner = unittest.TextTestRunner()
#    runner.run(suite)