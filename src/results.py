# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 09:58:47 2017

@author: Calil
"""

import numpy as np
import matplotlib.pyplot as plt

class Results(object):
    
    def __init__(self):
        
        self.__snir = []
        
    def add_snir(self,snir_vec):
        self.__snir.append(snir_vec)
        
    def plot_snir_cdf(self):
        ax, val =  self._plot_cdf(self.__snir)
        
        ax.set_xlabel("SNIR [dB]")
        ax.set_ylabel("CDF of SNIR")
        ax.set_xlim([np.min(val),np.max(val)])
        ax.set_ylim([0,1])
        ax.xaxis.grid(True)
        ax.yaxis.grid(True)
        
        return ax
        
    def _plot_cdf(self,val_list):
        val = np.ravel(np.array(val_list))
        val = np.sort(val)
        p_val = np.arange(0,len(val))/len(val)
        
        fig = plt.figure(figsize=(6,6))
        ax = fig.add_subplot(111)
        
        ax.plot(val,p_val)
        
        return ax, val
        
    def reset(self):
        self.__snir = []
        
    @property
    def snir(self):
        return self.__snir