# -*- coding: utf-8 -*-
"""
Created on Mon May 22 15:27:08 2017

@author: Calil
"""

import numpy as np
import numpy.testing as npt
import unittest

from base_station import BaseStation
from mobile_station import MobileStation

class BaseStationTest(unittest.TestCase):
    
    def setUp(self):
        # Create BS 1
        pos = np.array([100, 200, 10])
        azi = 60
        tilt = -10
        power = 40
        idx = 5
        self.bs1 = BaseStation(pos,azi,tilt,power,idx)
        
    def test_connect_to(self):
        
        pos = np.array([150, -200, 2])
        power = 20
        idx = 0
        ms0 = MobileStation(pos,power,idx)
        
        self.bs1.connect_to(ms0)
        self.assertEqual(len(self.bs1.ms_list),1)
        self.assertEqual(self.bs1.ms_list[0].idx,0)
        
        idx = 1
        ms1 = MobileStation(pos,power,idx)
        self.bs1.connect_to(ms1)
        self.assertEqual(len(self.bs1.ms_list),2)
        self.assertEqual(self.bs1.ms_list[0].idx,0)
        self.assertEqual(self.bs1.ms_list[1].idx,1)
        
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