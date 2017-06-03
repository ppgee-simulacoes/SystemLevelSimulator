# -*- coding: utf-8 -*-
"""
Created on Thu May 18 11:34:15 2017

@author: Calil
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection

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
            set_base_stations:
                Creates BS objects according to exagonal topology.
                Syntax: bs_list = self.get_base_stations()
                Outputs: bs_list <list>: list containing all the BS objects
                
        Author: Calil Queiroz
                calil_queiroz@hotmail.com
                
        Version History:
            V. 0.1 (May 18 2017) - create class skeleton 
    """
    
    def __init__(self, param):
        
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
                    x_row = 2*self.__h*np.arange(-max_x,max_x) + self.__h
                    max_x = max_x - 1
                else:
                    x_row = 2*self.__h*np.arange(-max_x,max_x+1)
                y_row = (k+1)*(1.5*self.__r)*np.ones_like(x_row)
                
                self.__x = np.append(self.__x,x_row)
                self.__y = np.append(self.__y,y_row)
                self.__x = np.append(self.__x,x_row)
                self.__y = np.append(self.__y,-y_row)
                
            for k in range(len(self.__x)):
                pos = np.array([self.__x[k], self.__y[k], self.__bs_height])
                # TODO: define azimuth and tilt angles
                azi = 0.0
                tilt = 0.0
                power = self.param.bs_power
                self.__bs_list.append(BaseStation(pos,azi,tilt,power,k))

        return self.__bs_list

    def plot_topology(self):
        
        fig = plt.figure(figsize=(6,6))
        ax = fig.add_subplot(111)
        
        patches = []
        hex_coord = np.array([[ self.__h, self.__r/2],
                              [ 0.0     , self.__r  ],
                              [-self.__h, self.__r/2],
                              [-self.__h,-self.__r/2],
                              [ 0.0,     -self.__r  ],
                              [ self.__h,-self.__r/2]])
        for k in range(self.__num_bs):
            hx = np.copy(hex_coord)
            hx[:,0] = hx[:,0] + self.__x[k]
            hx[:,1] = hx[:,1] + self.__y[k]
            poly = Polygon(hx,True)
            patches.append(poly)
        
        p = PatchCollection(patches, cmap='Greys', alpha=1.0,\
                            edgecolors='#000000')
        colors = np.zeros(len(patches))
        p.set_array(np.array(colors))
        
        ax.add_collection(p)
                
        ax.scatter(self.__x,self.__y,color='k')
        
        ax.set_xlabel("x axis [meters]")
        ax.set_ylabel("y axis [meters]")
        ax.set_xlim([np.min(self.__x)-self.__h,np.max(self.__x)+self.__h])
        ax.set_ylim([np.min(self.__y)-self.__r,np.max(self.__y)+self.__r])
        ax.xaxis.grid(True)
        ax.yaxis.grid(True)
#        plt.show()
        return ax
    
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
