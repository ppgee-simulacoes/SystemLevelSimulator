# -*- coding: utf-8 -*-
"""
Created on Mon May 22 15:27:08 2017

@author: Calil
"""

import numpy as np
import numpy.testing as npt
import unittest

from base_station import BaseStation

class BaseStationTest(unittest.TestCase):
    
    def setUp(self):
        # Create BS 1
        pos = np.array([100, 200, 10])
        azi = 60
        tilt = -10
        power = 40
        idx = 5
        self.bs1 = BaseStation(pos,azi,tilt,power,idx)
        
    def test_position(self):
        npt.assert_equal(self.bs1.position,np.array([100, 200, 10]))
        
    def test_tx_power(self):
        self.assertEqual(self.bs1.tx_power,40)
        
    def test_down_tilt(self):
        self.assertEqual(self.bs1.down_tilt,-10)
        
    def test_azimuth(self):
        self.assertEqual(self.bs1.azimuth,60)
        
    def test_ms_list(self):
        self.assertEqual(len(self.bs1.ms_list),0)
        
    def test_idx(self):
        self.assertEqual(self.bs1.idx,5)

if __name__ == '__main__':
    unittest.main()