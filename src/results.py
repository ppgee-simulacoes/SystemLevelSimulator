# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 09:58:47 2017

@author: Calil
"""

import numpy as np
import matplotlib.pyplot as plt

class Results(object):
    """
        Saves simulation results and plots CDFs.
        
        Properties:
            snir <list>: simulation SNIR values
            
        Constructor:
            Syntax: self = Results()
            
        Methods:
            add_snir:
                Store SNIR values for future ploting.
                Syntax: self.add_snir(snir_vec)
                Inputs: snir_vec <np.array>: vector containing SNIR values
                
        Author: Calil Queiroz
                calil_queiroz@hotmail.com
                
        Version History:
            V. 0.1 (Jun 15 2017) - create class 
    """
    
    def __init__(self,tput_loss,band):
        
        self.__snir = []
        self.__tput_loss = tput_loss
        self.__band = band
        
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
    
    def plot_tput(self):
        snir_val = np.ravel(np.array(self.__snir)) - self.__tput_loss
        snir_val = 10**(snir_val/10)
        tput = self.__band*np.log2(1 + snir_val)
        
        ax, val = self._plot_cdf(tput)
        
        ax.set_xlabel("Throughput [bps]")
        ax.set_ylabel("CDF of Throughput")
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