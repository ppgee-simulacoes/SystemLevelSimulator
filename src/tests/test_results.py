# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 10:26:44 2017

@author: Calil
"""

import unittest
import numpy as np
import matplotlib.pyplot as plt

from results import Results

class ResultsTest(unittest.TestCase):
    
    def setUp(self):
        
        self.plot_flag = True
        
        self.results = Results()
        
    def test_snir(self):
        self.assertEqual(len(self.results.snir),0)
        
    def test_add_snir(self):
        snir1 = np.array([1,2,3])
        self.results.add_snir(snir1)
        self.assertEqual(len(self.results.snir),1)
        
        snir2 = np.array([4,5,6])
        self.results.add_snir(snir2)
        self.assertEqual(len(self.results.snir),2)
        
    def test_plot_cdf_reset(self):
        snir1 = np.arange(0,50)
        self.results.add_snir(snir1)
        
        snir2 = np.arange(50,100)
        self.results.add_snir(snir2)
        
        ax = self.results.plot_snir_cdf()
        if(self.plot_flag): plt.show(ax)
        
        self.results.reset()
        snir1 = np.random.normal(size=1000)
        self.results.add_snir(snir1)
        
        snir2 = np.random.normal(size=1000)
        self.results.add_snir(snir2)
        
        ax = self.results.plot_snir_cdf()
        if(self.plot_flag): plt.show(ax)
        
if __name__ == '__main__':
    unittest.main()