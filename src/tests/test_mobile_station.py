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

if __name__ == '__main__':
    unittest.main()