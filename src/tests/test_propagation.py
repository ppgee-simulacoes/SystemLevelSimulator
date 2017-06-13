# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 14:48:06 2017

@author: Calil
"""

import unittest

from propagation import Propagation
from parameters.parameters import Parameters
from support.enumeration import PropagationModel, OkumuraEnv


class PropagationTest(unittest.TestCase):
    
    def setUp(self):
        self.param = Parameters()
        
        self.param.ref_loss = 3
        self.param.ref_distance = 1
        self.param.loss_coef = 2.5
        
        self.param.frequency = 700
        
        self.param.bs_height = 40
        self.param.ms_height = 1.5
        self.param.okumura_env = OkumuraEnv.URBAN
        
        self.param.shadowing_variance = 6
        
        self.param.propagation_model = PropagationModel.GENERIC
        self.propagation_generic = Propagation(self.param)
        
        self.param.propagation_model = PropagationModel.FREESPACE
        self.propagation_free = Propagation(self.param)
        
        self.param.propagation_model = PropagationModel.OKUMURA
        self.propagation_okumura = Propagation(self.param)
        
    def test_parameters(self):
        self.assertEqual(self.propagation_generic.model,PropagationModel.GENERIC)
        self.assertEqual(self.propagation_generic.pl_d0,3)
        self.assertEqual(self.propagation_generic.d0,1)
        self.assertEqual(self.propagation_generic.alpha,2.5)
        
        self.assertEqual(self.propagation_free.model,PropagationModel.FREESPACE)
        self.assertEqual(self.propagation_free.freq,700)
        
        self.assertEqual(self.propagation_okumura.model,PropagationModel.OKUMURA)
        self.assertEqual(self.propagation_okumura.hte,40)
        self.assertEqual(self.propagation_okumura.hre,1.5)
        self.assertEqual(self.propagation_okumura.env,OkumuraEnv.URBAN)
        
if __name__ == '__main__':
    unittest.main()