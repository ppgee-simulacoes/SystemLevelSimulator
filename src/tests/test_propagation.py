# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 14:48:06 2017

@author: Calil
"""

import unittest
from numpy.random import RandomState

from propagation import Propagation
from parameters.parameters import Parameters
from support.enumeration import PropagationModel, OkumuraEnv


class PropagationTest(unittest.TestCase):
    
    def setUp(self):
        self.param = Parameters()
        self.state = RandomState(5)
        
        self.param.shadowing = False
        
        self.param.ref_loss = 3
        self.param.ref_distance = 1
        self.param.loss_coef = 2.5
        
        self.param.frequency = 700
        
        self.param.bs_height = 40
        self.param.ms_height = 1.5
        
        self.param.shadowing_variance = 6
        
        self.param.propagation_model = PropagationModel.GENERIC
        self.propagation_generic = Propagation(self.param,self.state)
        
        self.param.shadowing = True
        self.propagation_shadow = Propagation(self.param,self.state)
        self.param.shadowing = False
        
        self.param.propagation_model = PropagationModel.FREESPACE
        self.propagation_free = Propagation(self.param,self.state)
        
        self.param.propagation_model = PropagationModel.OKUMURA
        self.param.okumura_env = OkumuraEnv.SMALL_URBAN
        self.propagation_small = Propagation(self.param,self.state)
        
        self.param.propagation_model = PropagationModel.OKUMURA
        self.param.okumura_env = OkumuraEnv.LARGE_URBAN
        self.param.frequency = 700
        self.propagation_large_1 = Propagation(self.param,self.state)
        
        self.param.frequency = 200
        self.propagation_large_2 = Propagation(self.param,self.state)
        
        self.param.frequency = 1600
        self.propagation_large_3 = Propagation(self.param,self.state)
        
        self.param.frequency = 700
        self.param.okumura_env = OkumuraEnv.SUBURBAN
        self.propagation_sub = Propagation(self.param,self.state)
        
        self.param.okumura_env = OkumuraEnv.RURAL
        self.propagation_rural = Propagation(self.param,self.state)
        
    def test_parameters(self):
        self.assertEqual(self.propagation_generic.model,PropagationModel.GENERIC)
        self.assertEqual(self.propagation_generic.pl_d0,3)
        self.assertEqual(self.propagation_generic.d0,1)
        self.assertEqual(self.propagation_generic.alpha,2.5)
        self.assertFalse(self.propagation_generic.shadow_flag)
        
        self.assertEqual(self.propagation_free.model,PropagationModel.FREESPACE)
        self.assertEqual(self.propagation_free.freq_mhz,700)
        self.assertEqual(self.propagation_free.freq_ghz,0.7)
        
        self.assertEqual(self.propagation_small.model,PropagationModel.OKUMURA)
        self.assertEqual(self.propagation_small.hte,40)
        self.assertEqual(self.propagation_small.hre,1.5)
        self.assertEqual(self.propagation_small.env,OkumuraEnv.SMALL_URBAN)
        
        self.assertEqual(self.propagation_large_1.model,PropagationModel.OKUMURA)
        self.assertEqual(self.propagation_large_1.hte,40)
        self.assertEqual(self.propagation_large_1.hre,1.5)
        self.assertEqual(self.propagation_large_1.env,OkumuraEnv.LARGE_URBAN)
        
    def test_shadowing(self):
        eps = 1e-2
        d = 5000
        
        # Test shadowing: since the shadowing loss is a random variable, this
        # test only indicates changes in the variable value and cannot be used
        # to dictate its correctness.
        self.assertAlmostEqual(self.propagation_shadow.propagate(d),21.555,delta=eps)
        
    def test_propagate(self):
        eps = 1e-2
        d = 5000
        
        # Test generic model
        self.assertAlmostEqual(self.propagation_generic.propagate(d),20.474,delta=eps)
        
        # Test free space model
        self.assertAlmostEqual(self.propagation_free.propagate(d),103.321,delta=eps)
        
        # Okumura-Hata/COST test
        # Small urban scenario
        self.assertAlmostEqual(self.propagation_small.propagate(d),99.034,delta=eps)
        
        # Large urban scenario
        # fc = 700 MHz
        self.assertAlmostEqual(self.propagation_large_1.propagate(d),99.041,delta=eps)
        
        # fc = 200 MHz
        self.assertAlmostEqual(self.propagation_large_2.propagate(d),84.572,delta=eps)
        
        # fc = 1600 MHz
        self.assertAlmostEqual(self.propagation_large_3.propagate(d),159.827,delta=eps)
        
        # Suburban scenario
        self.assertAlmostEqual(self.propagation_sub.propagate(d),89.726,delta=eps)
        
        # Rural scenario
        self.assertAlmostEqual(self.propagation_rural.propagate(d),-32.789,delta=eps)
        
if __name__ == '__main__':
    unittest.main()