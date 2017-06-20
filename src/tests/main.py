# -*- coding: utf-8 -*-
"""
Created on Tue May 23 17:35:39 2017

@author: Calil
"""

import unittest

loader = unittest.TestLoader()
tests = loader.discover('.')
testRunner = unittest.runner.TextTestRunner()
testRunner.run(tests)