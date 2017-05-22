# -*- coding: utf-8 -*-
"""
Created on Mon May 22 15:27:08 2017

@author: Calil
"""

import numpy as np
import numpy.testing as npt
import unittest

from base_station import BaseStation
from parameters import Parameters

class BaseStationTest(unittest.TestCase):
    
    def setUp(self):
        self.par = Parameters
        self.par.bs_height = 10
        self.par.bs_azimuth = [60, 180, 300]
        self.par.bs_down_tilt = -10
        self.par.bs_power = 40
        
        # Create BS
        pos = np.array([100, 200, 300])
        self.bs1 = BaseStation(pos,self.par.bs_azimuth[0],self.par)
        
    def test_position(self):
        npt.assert_equal(self.bs1.position,np.array([100, 200, 300]))
        
    def test_tx_power(self):
        self.assertEqual(self.bs1.tx_power,40)
        
    def test_down_tilt(self):
        self.assertEqual(self.bs1.down_tilt,-10)
        
    def test_azimuth(self):
        self.assertEqual(self.bs1.azimuth,60)
        
    def test_ms_list(self):
        self.assertEqual(len(self.bs1.ms_list),0)

if __name__ == '__main__':
    unittest.main()