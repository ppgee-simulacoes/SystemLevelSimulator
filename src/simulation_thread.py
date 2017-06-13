# -*- coding: utf-8 -*-
"""
Created on Thu May 18 11:04:05 2017

@author: Calil
"""

import numpy as np
import itertools as itls
import matplotlib.pyplot as plt

from support.enumeration import SimType, RandomSeeds
from topology import Topology
from mobile_station import MobileStation
from propagation import Propagation

class SimulationThread(object):
    """
        Performs simulation thread, with multiple drops.
        
        Properties:
            param <Parameters>: simulation parameters
            topology <Topology>: network toloplogy and BS positions
            bs_list <list>: list of all the BS objects
            ms_list <list>: list of all MS objects
            
        Constructor:
            Syntax: self = SimulationThread(param)
            Inputs: param <Parameters>: simulation parameters
            
        Methods:
            create_ms:
                Uses topology to create MS objects and save them in ms_list
                property.
                
        Author: Calil Queiroz
                calil_queiroz@hotmail.com
                
        Version History:
            V. 0.1 (May 18 2017) - create class skeleton  
    """

    def __init__(self, param):
        
        self.param = param

        self.__seed_count = 0

        self.__seed = self.param.seeds[self.__seed_count]
        self.__seed_set = self.param.seed_set
        self.__random_states = self.initialize_random_states()

        self.__num_ms = param.num_ms
        
        self.topology = Topology(param)
        self.__bs_list = self.topology.set_base_stations()
        
        self.propagation = Propagation(param,\
            self.__random_states[RandomSeeds.MOBILE_POSITION.value])
        
        self.__ms_list = []

        self.__grid_R = 0
        
        self.__x_ms = np.empty(self.__num_ms)
        self.__y_ms = np.empty(self.__num_ms)
        
        self.__bs_ms_x = [[] for k in range(self.topology.num_bs)]
        self.__bs_ms_y = [[] for k in range(self.topology.num_bs)]
        self.__connected = False

    def simulate(self):

        # Perform Loop
        self.run_loop()

        # Save results in future releases

    def run_loop(self):

        drop_number = 1
        if self.param.simulation_type is SimType.FIXED_SEEDS:
            while drop_number <= self.param.max_num_drops:
                # Print drop number to screen
                print("Running drop number {}...".format(drop_number))

                self.create_ms()
                self.connect_ms_to_bs()
                self.plot_grid()
                plt.show()

                self.reset_state()

                drop_number += 1

        elif self.param.simulation_type is SimType.FIXED_CONF:
            return NotImplemented

        else:
            raise NameError('Unknown simulation type!')

    def create_ms(self):
        
        max_idx = np.argmax(self.topology.y)
        y_max = self.topology.y[max_idx] + self.topology.r
        x_max = self.topology.x[max_idx]
        
        self.__grid_R = np.sqrt(x_max**2 + y_max**2)
        theta = self.__random_states[RandomSeeds.MOBILE_POSITION.value].\
            uniform(0, 2*np.pi, self.__num_ms)
        r = self.__grid_R * np.sqrt(self.__random_states[RandomSeeds.MOBILE_POSITION.value].
                                    uniform(0, 1, self.__num_ms))
        
        self.__x_ms = r*np.cos(theta)
        self.__y_ms = r*np.sin(theta)
        
        for k in range(self.__num_ms):
            pos = np.array([self.__x_ms[k], self.__y_ms[k], self.param.ms_height])
            self.__ms_list.append(MobileStation(pos,self.param.ms_tx_power,k))
            
    def connect_ms_to_bs(self):
        for ms in self.__ms_list:
            max_pow = -np.inf
            bs_to_connect = None
            for bs in self.__bs_list:
                p_vec = np.array([(ms.position[0]-bs.position[0]),\
                                   ms.position[1]-bs.position[1]])
                dist = np.sqrt(p_vec[0]**2 + p_vec[1]**2)
                power = bs.tx_power - self.propagation.propagate(dist)
                if(power > max_pow):
                    max_pow = power
                    bs_to_connect = bs
            ms.connected_to = bs_to_connect
            bs_to_connect.connect_to(ms)
            self.__bs_ms_x[bs_to_connect.idx].append(ms.position[0])
            self.__bs_ms_y[bs_to_connect.idx].append(ms.position[1])
        self.__connected = True
            
    def plot_grid(self):
        ax = self.topology.plot_topology()
        if(self.__connected):
            colors = itls.cycle(['r', 'g', 'm', 'y', 'c', 'b', 'grey', 'orange', 'teal'])
            for k in range(self.topology.num_bs):
                clr = next(colors)
                ax.scatter(self.__bs_ms_x[k],self.__bs_ms_y[k], s = 9, color=clr)
        else:
            ax.scatter(self.__x_ms,self.__y_ms, s = 9,color='red')
        
        theta = np.linspace(0,2*np.pi,num=100)
        circle_x = self.__grid_R*np.cos(theta)
        circle_y = self.__grid_R*np.sin(theta)
        
        ax.plot(circle_x,circle_y,'k',linewidth = 0.5)
        
        ax.set_xlim([min(circle_x),max(circle_x)])
        ax.set_ylim([min(circle_y),max(circle_y)])
        
        return ax

    def initialize_random_states(self):

        num_states = len(self.param.state_indexes)
        random_states = []

        for index in range(0, num_states):
            state_seed = self.__seed_set[self.__seed + index]
            random_states.append(np.random.RandomState(state_seed))

        return random_states

    def reset_state(self):

        self.__seed_count += 1

        if self.__seed_count < len(self.param.seeds):
            self.__seed = self.param.seeds[self.__seed_count]
            self.__random_states = self.initialize_random_states()
            
        self.propagation.rand_state = self.__random_states[RandomSeeds.MOBILE_POSITION.value]


    @property
    def seed(self):
        return self.__seed

    @property
    def seed_set(self):
        return self.__seed_set

    @property
    def random_states(self):
        return self.__random_states

    @property
    def num_ms(self):
        return self.__num_ms
    
    @property
    def bs_list(self):
        return self.__bs_list
    
    @property
    def ms_list(self):
        return self.__ms_list
    
    @property
    def x_ms(self):
        return self.__x_ms
    
    @property
    def y_ms(self):
        return self.__y_ms
    
    @property
    def bs_ms_x(self):
        return self.__bs_ms_x
    
    @property
    def bs_ms_y(self):
        return self.__bs_ms_y

