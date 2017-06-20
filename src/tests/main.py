# -*- coding: utf-8 -*-
"""
Created on Tue May 23 17:35:39 2017

@author: Calil
"""

#import unittest

#loader = unittest.TestLoader()
#tests = loader.discover('.')
#testRunner = unittest.runner.TextTestRunner()
#testRunner.run(tests)

from parameters.parameters import Parameters
from simulation_thread import SimulationThread

#figs_dir = "figs/"

param = Parameters()
sim_thread = SimulationThread(param)

sim_thread.simulate()