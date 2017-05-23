# -*- coding: utf-8 -*-
"""
Created on Thu May 18 11:34:15 2017

@author: Calil
"""

import numpy as np

from base_station import BaseStation

class Topology(object):
    """
        Generates simulation topology, calculating the position of the BSs.
        
        Properties:
            radius <1x1 float>: cell radius [meters]
            num_layers <1x1 int>: number of interference layers
            bs_list <1xN list>: list of all BSs
            
        Constructor:
            Syntax: self = Topology(param)
            Inputs: param <Parameters>: simulation parameters
                    
        Methods:
            get_base_stations:
                Creates BS objects according to exagonal topology.
                Syntax: bs_list = self.get_base_stations()
                Outputs: bs_list <list>: list containing all the BS objects
                
        Author: Calil Queiroz
                calil_queiroz@hotmail.com
                
        Version History:
            V. 0.1 (May 18 2017) - create class skeleton 
    """
    
    def __init__(self,param):
        
        self.param = param
        self.__bs_height = param.bs_height
        
        self.__r = param.cell_radius
        self.__num_layers = param.num_layers
        self.__bs_list = []
        
        self.__s60 = np.sin(np.deg2rad(60))
        self.__c60 = np.cos(np.deg2rad(60))
        self.__h = self.__r*self.__s60
        
        self.__num_rows = 2*self.__num_layers + 1
        self.__max_hex = 2*self.__num_layers + 1
        self.__bot_row = self.__num_layers + 1
        
        self.__num_bs = 0
        for k in range(self.__bot_row,self.__max_hex):
            self.__num_bs = self.__num_bs + k
        self.__num_bs = 2*self.num_bs
        self.__num_bs = self.__num_bs + self.__max_hex
        
        self.__x = np.array([])
        self.__y = np.array([])
        
    def set_base_stations(self):
        if(len(self.__bs_list) == 0):
            
            max_x = np.floor(self.__max_hex/2) 
            self.__x = 2*self.__h*np.arange(-max_x,max_x+1)
            self.__y = np.zeros_like(self.__x)
            
            for k in range(self.__num_layers):
                if(k%2==0):
                    x_row = 2*self.__h*np.arange(-max_x,max_x+k) + self.__h
                else:
                    x_row = 2*self.__h*np.arange(-max_x,max_x+1)
                y_row = (k+1)*(1.5*self.__r)*np.ones_like(x_row)
                max_x = max_x - 1
                
                self.__x = np.append(self.__x,x_row)
                self.__y = np.append(self.__y,y_row)
                self.__x = np.append(self.__x,x_row)
                self.__y = np.append(self.__y,-y_row)
                
            for k in range(len(self.__x)):
                pos = np.array([self.__x[k], self.__y[k], self.__bs_height])
                azi = 0.0
                tilt = 0.0
                power = 0.0
                self.__bs_list.append(BaseStation(pos,azi,tilt,power))
            
        return self.__bs_list    
    
    @property
    def r(self):
        return self.__r
    
    @property
    def num_layers(self):
        return self.__num_layers
    
    @property
    def bs_list(self):
        return self.__bs_list
    
    @property
    def h(self):
        return self.__h
    
    @property
    def num_rows(self):
        return self.__num_rows
    
    @property
    def max_hex(self):
        return self.__max_hex
    
    @property
    def bot_row(self):
        return self.__bot_row
    
    @property
    def num_bs(self):
        return self.__num_bs
    
    @property
    def x(self):
        return self.__x
    
    @property
    def y(self):
        return self.__y
