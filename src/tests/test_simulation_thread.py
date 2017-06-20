# -*- coding: utf-8 -*-
"""
Created on Thu May 25 17:19:54 2017

@author: Calil
"""

import unittest
import matplotlib.pyplot as plt
import numpy.testing as npt
import numpy as np

from simulation_thread import SimulationThread
from parameters.parameters import Parameters
from support.enumeration import PropagationModel

class SimulationThreadTest(unittest.TestCase):
    
    def setUp(self):
        
        self.plot_flag = False
        
        self.param = Parameters()
        self.param.cell_radius = 200
        self.param.num_layers = 1
        self.param.bs_height = 10
        self.param.bs_azimuth = [60, 180, 300]
        self.param.bs_down_tilt = -10
        self.param.bs_power = 40
        self.param.num_ms = 50
        self.param.ms_height = 1.5
        self.param.ms_tx_power = 20
        self.param.seed_set = np.array([1])
        self.param.max_num_drops = 1
        self.param.seeds = [0]
        
        self.param.propagation_model = PropagationModel.FREESPACE
        self.param.frequency = 700
        self.param.shadowing = False
        
        self.sim_thread = SimulationThread(self.param)
        
        self.param.shadowing = True
        self.param.shadowing_variance = 20
        self.sim_thread_shadow = SimulationThread(self.param)
        
        self.param.shadowing = False
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
        self.assertEqual(self.sim_thread.seed,0)
        
    def test_bs_ms(self):
        self.assertEqual(len(self.sim_thread.bs_ms_x),7)
        self.assertEqual(len(self.sim_thread.bs_ms_y),7)
        
    def test_bs_rx(self):
        npt.assert_equal(self.sim_thread.bs_rx_power,np.zeros((7,50)))
        
    def test_create_ms(self):
        self.sim_thread.create_ms()
        self.assertEqual(len(self.sim_thread.ms_list),50)
        self.assertEqual(len(self.sim_thread.x_ms),50)
        self.assertEqual(len(self.sim_thread.y_ms),50)
        
        self.sim_thread_2.create_ms()
        self.assertEqual(len(self.sim_thread_2.ms_list),2)
        self.assertEqual(len(self.sim_thread_2.x_ms),2)
        self.assertEqual(len(self.sim_thread_2.y_ms),2)
        
    def test_connect_ms_to_bs(self):
        self.sim_thread_2.create_ms()
        self.sim_thread_2.connect_ms_to_bs()
        
        npt.assert_equal(np.shape(self.sim_thread_2.bs_rx_power),(1,2))
        self.assertTrue(np.all(self.sim_thread_2.bs_rx_power < \
                               self.sim_thread_2.ms_list[0].tx_power))
        
        self.assertEqual(self.sim_thread_2.ms_list[0].connected_to.idx,0)
        self.assertEqual(self.sim_thread_2.ms_list[1].connected_to.idx,0)
        self.assertEqual(self.sim_thread_2.bs_list[0].ms_list[0].idx,0)
        self.assertEqual(self.sim_thread_2.bs_list[0].ms_list[1].idx,1)
        
        self.sim_thread_3.create_ms()
        self.sim_thread_3.connect_ms_to_bs()
        npt.assert_equal(np.shape(self.sim_thread_3.bs_rx_power),(19,200))
        self.assertTrue(np.all(self.sim_thread_3.bs_rx_power < \
                               self.sim_thread_3.ms_list[0].tx_power))
        
    def test_select_mss_snir(self):
        self.sim_thread_2.create_ms()
        self.sim_thread_2.connect_ms_to_bs()
        self.sim_thread_2.select_mss()
        
        self.assertEqual(len(self.sim_thread_2.active_mss_idx),1)
        self.assertAlmostEqual(self.sim_thread_2.calculate_snir(),29.832,delta=1e-2)
        
        self.sim_thread_3.create_ms()
        self.sim_thread_3.connect_ms_to_bs()
        self.sim_thread_3.select_mss()
        
        self.assertEqual(len(self.sim_thread_3.active_mss_idx),19)
        self.assertEqual(len(self.sim_thread_3.calculate_snir()),19)
        
    def test_reset(self):
        self.sim_thread_3.create_ms()
        self.sim_thread_3.connect_ms_to_bs()
        self.sim_thread_3.select_mss()
        snir = self.sim_thread_3.calculate_snir()
        self.sim_thread_3.results.add_snir(snir)
        
        self.sim_thread_3.reset_grid()
        
        self.assertEqual(np.sum(self.sim_thread_3.bs_rx_power),0.0)
        self.assertEqual(len(self.sim_thread_3.ms_list),0)
        self.assertEqual(len(self.sim_thread_3.active_mss_idx),0)
        self.assertEqual(np.sum(self.sim_thread_3.x_ms),0.0)
        self.assertEqual(np.sum(self.sim_thread_3.y_ms),0.0)
        self.assertEqual(len(np.ravel(np.array(self.sim_thread_3.bs_ms_x))),0)
        self.assertEqual(len(np.ravel(np.array(self.sim_thread_3.bs_ms_y))),0)
        
    def test_plot_grid(self):
        self.sim_thread.create_ms()
        ax = self.sim_thread.plot_grid()
        if(self.plot_flag): plt.show(ax)
        
        self.sim_thread.connect_ms_to_bs()
        ax = self.sim_thread.plot_grid()
        if(self.plot_flag): plt.show(ax)
               
        self.sim_thread_shadow.create_ms()
        self.sim_thread_shadow.connect_ms_to_bs()
        ax = self.sim_thread_shadow.plot_grid()
        if(self.plot_flag): plt.show(ax)
        
        self.sim_thread_3.create_ms()
        self.sim_thread_3.connect_ms_to_bs()
        ax = self.sim_thread_3.plot_grid()
        if(self.plot_flag): plt.show(ax)
        
    def test_simulate(self):
        pass
        
if __name__ == '__main__':
    unittest.main()
    
#    suite = unittest.TestSuite()
#    suite.addTest(SimulationThreadTest("test_plot_grid"))
#    runner = unittest.TextTestRunner()
#    runner.run(suite)