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
from results import Results

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
            V. 1.0 (Jun 20 2017) - add Downlink SNIR
    """

    def __init__(self, param):
        
        self.param = param

        self.__seed_count = 0

        self.__seed = self.param.seeds[self.__seed_count]
        self.__seed_set = self.param.seed_set
        self.__random_states = self.initialize_random_states()
        
        self.topology = Topology(param)
        self.__bs_list = self.topology.set_base_stations()
        
        self.__num_ms = param.num_ms
        self.__num_bs = self.topology.num_bs
        
        self.propagation = Propagation(param,\
            self.__random_states[RandomSeeds.MOBILE_POSITION.value])
        self.results = Results()
        
        self.__bs_rx_power = np.zeros((self.__num_bs,self.__num_ms))
        self.__ms_rx_power = np.zeros((self.__num_bs, self.__num_ms))

        self.__ms_list = []
        
        self.__active_mss_idx = []

        self.__grid_R = 0
        
        self.__x_ms = np.zeros(self.__num_ms)
        self.__y_ms = np.zeros(self.__num_ms)
        
        self.__bs_ms_x = [[] for k in range(self.topology.num_bs)]
        self.__bs_ms_y = [[] for k in range(self.topology.num_bs)]
        self.__connected = False

    def simulate(self):

        # Perform Loop
        self.run_loop()

        # Save results in future releases
        ax2 = self.results.plot_snir_cdf()
        plt.show(ax2)

    def run_loop(self):

        drop_number = 1
        if self.param.simulation_type is SimType.FIXED_SEEDS:
            while drop_number <= self.param.max_num_drops:
                # Print drop number to screen
                print("Running drop number {}...".format(drop_number))

                self.create_ms()
                self.connect_ms_to_bs()
                self.select_mss()
                #self.results.add_snir(self.calculate_snir())
                self.results.add_snir(self.calculate_snir_downlink())
                if (self.param.plot_drop_grid):
                    ax1 = self.plot_grid()
                    plt.show(ax1)

                self.reset_state()
                self.reset_grid()

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
                path_loss = self.propagation.propagate(dist)
                ms_rx_power = bs.tx_power - path_loss
                self.__ms_rx_power[bs.idx, ms.idx] = ms_rx_power
                self.__bs_idx = bs.idx
                bs_rx_power = ms.tx_power - path_loss
                self.__bs_rx_power[bs.idx,ms.idx] = bs_rx_power
                if(ms_rx_power > max_pow):
                    max_pow = ms_rx_power
                    bs_to_connect = bs
                    self.con_bs_idx = bs.idx
            ms.connected_to = bs_to_connect
            bs_to_connect.connect_to(ms)
            self.__bs_ms_x[bs_to_connect.idx].append(ms.position[0])
            self.__bs_ms_y[bs_to_connect.idx].append(ms.position[1])
        self.__connected = True

    def select_mss(self):
        for bs in self.__bs_list:
            num_con_mss = len(bs.ms_list)
            if(num_con_mss > 0):
                ue_idx = self.__random_states[RandomSeeds.MOBILE_POSITION.value].\
                randint(0,high=num_con_mss)
                bs.ms_list[ue_idx].active = True
                self.__active_mss_idx.append(bs.ms_list[ue_idx].idx)
            
    def calculate_snir(self):

        snir_vec = np.zeros(self.__num_bs)
        active_bss = []

        for bs in self.__bs_list:
            if(len(bs.ms_list) > 0):
                active_bss.append(bs.idx)
                rx_pow = self.__bs_rx_power[bs.idx,self.__active_mss_idx[bs.idx]]
                int_n = np.sum(10**(self.__bs_rx_power[bs.idx,self.__active_mss_idx]/10))\
                - 10**(rx_pow/10) + 10**(bs.noise/10)
                snir_vec[bs.idx] = rx_pow - 10*np.log10(int_n)

        return snir_vec[active_bss]

    def calculate_snir_downlink(self):
        snir_vec_downlink = np.zeros(self.__num_ms)
        active_mss = []

        for ms in self.__ms_list:
            active_mss.append(ms.idx)
            rx_pow = self.__ms_rx_power[self.con_bs_idx,ms.idx]
            int_n = np.sum(10 ** (self.__ms_rx_power[self.__bs_idx,ms.idx] / 10)) \
            - 10 ** (rx_pow / 10) + 10 ** (ms.noise / 10)
            snir_vec_downlink[ms.idx] = rx_pow - 10 * np.log10(int_n)

        return snir_vec_downlink[active_mss]
            
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
        
    def reset_grid(self):
        self.__bs_rx_power = np.zeros((self.__num_bs,self.__num_ms))
        self.__ms_rx_power = np.zeros((self.__num_bs, self.__num_ms))

        self.__ms_list = []
        
        self.__active_mss_idx = []
        
        self.__x_ms = np.zeros(self.__num_ms)
        self.__y_ms = np.zeros(self.__num_ms)
        
        self.__bs_ms_x = [[] for k in range(self.topology.num_bs)]
        self.__bs_ms_y = [[] for k in range(self.topology.num_bs)]
        self.__connected = False


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
    def num_bs(self):
        return self.__num_bs
    
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
    
    @property
    def bs_rx_power(self):
        return self.__bs_rx_power

    @property
    def ms_rx_power(self):
        return self.__ms_rx_power

    @property
    def active_mss_idx(self):
        return self.__active_mss_idx