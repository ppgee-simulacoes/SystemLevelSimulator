# -*- coding: utf-8 -*-
"""
Created on Thu May 25 16:56:33 2017

@author: Calil
"""

import numpy as np
import numpy.testing as npt
import unittest

from base_station import BaseStation
from mobile_station import MobileStation

class MobileStationTest(unittest.TestCase):
    
    def setUp(self):
        # Create MS 1
        pos = np.array([150, -200, 2])
        power = 20
        idx = 2
        self.ms1 = MobileStation(pos,power,idx)
        
    def test_position(self):
        npt.assert_equal(self.ms1.position,np.array([150, -200, 2]))
        
    def test_tx_power(self):
        self.assertEqual(self.ms1.tx_power,20)
        
    def test_idx(self):
        self.assertEqual(self.ms1.idx,2)
        
    def test_connected_to(self):
        self.assertEqual(self.ms1.connected_to,None)
        
        pos = np.array([100, 200, 10])
        azi = 60
        tilt = -10
        power = 40
        idx = 5
        bs = BaseStation(pos,azi,tilt,power,idx)
        self.ms1.connected_to = bs
        
        npt.assert_equal(self.ms1.connected_to.position,np.array([100, 200, 10]))
        self.assertEqual(self.ms1.connected_to.tx_power,40)
        self.assertEqual(self.ms1.connected_to.down_tilt,-10)
        self.assertEqual(self.ms1.connected_to.azimuth,60)
        self.assertEqual(self.ms1.connected_to.idx,5)
        

if __name__ == '__main__':
    unittest.main()