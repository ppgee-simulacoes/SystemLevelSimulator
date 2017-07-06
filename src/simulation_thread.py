

import numpy as np
import itertools as itls
import matplotlib.pyplot as plt

from support.enumeration import SimType, RandomSeeds
from topology import Topology
from base_station import BaseStation
from mobile_station import MobileStation
from path_loss import PathLoss
from results import Results


class SimulationThread(object):
    """
        SimulationThread is a class that creates the simulation thread 
        and runs the simulation for multiple drops.
        
        Properties:
            seed <1x1 int>: simulation seed position in set for current drop
            seed_set <1xset_size int list>: list of all available simulation seeds
            random_states <1xnum_states RandomState list>: list of all RandomState objects
            num_ms <1x1 int>: total number of MSs
            num_bs <1x1 int>: total number of BSs
            topology <Topology>: network topology with BSs positions
            bs_list <1xnum_bs BaseStation list>: list of all BS objects
            ms_list <1xnum_ms MobileStation list>: list of all MS objects
            grid_radius <1x1 float>: grid radius in meters
            connected <1x1 logic>: indicator of end of connection method
            
        Constructor:
            Syntax: self = SimulationThread(parameters)
            Inputs: parameters <Parameters>: simulation parameters
            
        Methods:
            simulate:
                Simulates the system for given parameters and saves the results
                Syntax: self.simulate()
            
            run_loop:
                Runs the main simulation drop loop for each given seed until criteria is met
                Syntax: self.run_loop()
                
            create_ms:
                Uses topology to create MS objects uniformly distributed inside grid
                Syntax: self.create_ms()
                
            connect_ms_to_bs:
                Connects each MS to an available BS according to received signal power level
                Syntax: self.connect_ms_to_bs()
                
            plot_grid:
                Plots cell grid with BS and MS distribution
                Syntax: self.plot_grid()
                
            initialize_random_states:
                Initialize each random state from seed in seed set
                Syntax: self.initialize_random_states()
                
            reset_state:
                Resets simulation loop for a new seed and reinitialize random states and lists of objects
                Syntax: self.reset_state()
                
        Author: Artur Rodrigues
                artur.rodrigues@ieee.org
                Calil Queiroz
                calil_queiroz@hotmail.com
                
        Version History:
            V. 0.1 (May 18 2017) - create class skeleton  
            V. 0.2 (June 01 2017) - added drop loop
    """

    def __init__(self, parameters):

        self.parameters = parameters

        self.__seed_count = 0

        self.__seed = self.parameters.seeds[self.__seed_count]
        self.__seed_set = self.parameters.seed_set
        self.__random_states = self.initialize_random_states()

        self.__num_ms = parameters.num_ms

        self.topology = Topology(self.parameters.cell_radius,
                                 self.parameters.num_layers,
                                 self.parameters.bs_height)

        self.path_loss = PathLoss(self.parameters, self.random_states[RandomSeeds.SHADOWING.value])

        self.results = Results()

        self.__num_bs, bs_coordinates = self.topology.set_bs_positions()

        self.__bs_list = []

        bs_index = 0
        for bs in range(0, self.num_bs):
            for azimuth_index, azimuth in enumerate(self.parameters.bs_azimuth):
                self.__bs_list.append(BaseStation(bs_coordinates[bs], azimuth,
                                                  self.parameters.bs_down_tilt, self.parameters.bs_power,
                                                  self.parameters.bs_n0, azimuth_index,
                                                  self.parameters.frequency_bands[azimuth_index],
                                                  bs_index))
                bs_index += 1

        self.__ms_list = []

        # Calculate approximate grid radius
        x_max, y_max = self.topology.xy_coordinates[0]
        x_max -= self.topology.cell_side
        y_max += self.topology.cell_radius/2
        self.__grid_radius = np.sqrt(abs(x_max) ** 2 + abs(y_max) ** 2)

        self.__connected = False

    def simulate(self):

        # Perform Loop
        self.run_loop()
        # Save results in future releases
        throughput_ul, snir_ul, \
        throughput_dl, snir_dl = self.results.plot_statistics_cdf()

        plt.show(throughput_dl)
        plt.show(snir_dl)
        plt.show(throughput_ul)
        plt.show(snir_ul)

    def run_loop(self):

        drop_number = 1
        if self.parameters.simulation_type is SimType.FIXED_SEEDS:
            while drop_number <= self.parameters.max_num_drops:
                # Print drop number to screen
                print("Running drop number {}...".format(drop_number))

                # Creates the MSs in random positions
                self.create_ms()
                # Connects the MSs to each BSs according to the received power
                self.connect_ms_to_bs()
                # Get SNIR Vector from current drop
                statistics_DL, statistics_UL = self.get_statistics()
                # Save statistics from current drop
                self.results.add_statistics(statistics_DL, statistics_UL)
                # Plots the Simulation Grid
                if self.parameters.plot_drop_grid:
                    grid = self.plot_grid()
                    plt.show(grid)
                # Resets all RandomStates and MS objects
                self.reset_state()

                drop_number += 1

        elif self.parameters.simulation_type is SimType.FIXED_CONF:
            return NotImplemented

        else:
            raise NameError('Unknown simulation type!')

    def create_ms(self):

        # Calculate position of MS for uniform distribution
        theta = (self.__random_states[RandomSeeds.MOBILE_POSITION.value].
                 uniform(0, 2 * np.pi, self.__num_ms))
        r_aux = self.grid_radius * np.sqrt(self.__random_states[RandomSeeds.MOBILE_POSITION.value].
                                           uniform(0, 1, self.__num_ms))

        xy_positions = list(zip(r_aux * np.cos(theta), r_aux * np.sin(theta)))

        for ms_index in range(0, self.__num_ms):
            x, y = xy_positions[ms_index]
            ms_coordinates = np.array([x, y, self.parameters.ms_height])
            self.__ms_list.append(MobileStation(ms_coordinates,
                                                self.parameters.ms_power,
                                                self.parameters.ms_n0,
                                                self.parameters.ms_bandwidth,
                                                ms_index))

    def connect_ms_to_bs(self):

        for ms in self.__ms_list:

            # Initialize for minimum received power and chosen BS
            power_max = -np.inf
            bs_to_connect = None

            for bs in self.__bs_list:
                # Get MS distance for each BS
                relative_position = np.array([(ms.position[0] - bs.position[0]),
                                              ms.position[1] - bs.position[1]])
                distance = np.sqrt(relative_position[0] ** 2 + relative_position[1] ** 2)

                # Calculate antenna gains
                if self.parameters.sectorization:
                    antenna_gain = bs.calculate_antenna_gain(ms.position)
                else:
                    antenna_gain = 0

                # Calculate path loss and received power for different propagation models
                path_loss = self.path_loss.calculate_path_loss(distance)

                # Received power at the MS and BS, respectively
                ms_rx_power = bs.tx_power - path_loss + antenna_gain
                bs_rx_power = ms.tx_power - path_loss + antenna_gain

                ms.interference_power.append(ms_rx_power)

                bs.interference_power.append(bs_rx_power)

                # Choose BS with maximum received power
                if ms_rx_power > power_max:
                    power_max = ms_rx_power
                    bs_to_connect = bs
                    bs_to_connect_rx_power = bs_rx_power

            # Connect MS with corresponding BS
            self.bs_list[bs_to_connect.index].connect_to(ms)
            self.bs_list[bs_to_connect.index].get_rx_power(bs_to_connect_rx_power)

            ms.connect_to(bs_to_connect)

            # Save Received Power and Interference Power for each MS
            ms.rx_power = power_max
            ms.interference_power.sort()
            del ms.interference_power[-1]

        self.__connected = True

    def get_bs_interference(self, current_bs):

        # Create vector of interference power from each BS
        interference_power_vector = np.zeros(len(self.bs_list))
        for bs in self.bs_list:
            num_connected_ms = len(bs.connected_ms_list)
            # Interference occurs only if there are MSs connected to the BS and it is not using the same band
            if num_connected_ms > 0 and bs.tx_band_index == current_bs.tx_band_index:
                # Choose random connected MS as the active at interference level
                active_ms_index = self.random_states[RandomSeeds.ACTIVE_MOBILE.value].\
                    randint(0, high=num_connected_ms)
                active_ms = bs.connected_ms_list[active_ms_index]
                active_ms_power = current_bs.interference_power[active_ms.index]
                interference_power_vector[bs.index] = active_ms_power

        return interference_power_vector

    def get_statistics(self):

        snir_vector_DL = np.zeros(self.__num_ms)
        throughput_DL = np.copy(snir_vector_DL)
        snir_vector_UL = np.zeros(len(self.bs_list))
        throughput_UL = np.copy(snir_vector_UL)

        for ms in self.ms_list:
            # Get SNIR for each MS
            snir_vector_DL[ms.index], throughput_DL[ms.index] = ms.calculate_statistics()

        for bs in self.bs_list:
            # Get vector of interference power and delete element corresponding to current BS
            bs.selected_interference_power = np.delete(self.get_bs_interference(bs), bs.index)
            if bs.connected_ms_list:
                snir_vector_UL[bs.index], \
                throughput_UL[bs.index] = bs.calculate_statistics(self.random_states[RandomSeeds.ACTIVE_MOBILE.value])

        # Eliminate BSs that are not causing interference
        snir_vector_UL = np.delete(snir_vector_UL, np.where(snir_vector_UL == 0))
        throughput_UL = np.delete(throughput_UL, np.where(throughput_UL == 0))

        statistics_DL = snir_vector_DL, throughput_DL
        statistics_UL = snir_vector_UL, throughput_UL

        return statistics_DL, statistics_UL

    def plot_grid(self):

        ax = self.topology.plot_topology()

        if self.__connected:

            colors = itls.cycle(['#800000', '#FF8C00', '#9ACD32', '#008B8B', '#1E90FF', '#4B0082',
                                 '#FF1493', '#8B4513', '#708090', '#FF0000', '#FFD700', '#7CFC00',
                                 '#00FFFF', '#87CEFA', '#8B008B', '#FF69B4', '#D2691E', '#B0C4DE',
                                 '#FF7F50', '#B8860B', '#006400', '#B0E0E6', '#000080', '#BA55D3',
                                 '#F5F5DC', '#F4A460', '#696969', '#BDB76B', '#CD5C5C', '#90EE90',
                                 '#4682B4', '#0000FF', '#EE82EE', '#F5DEB3', '#BC8F8F', '#A9A9A9',
                                 '#808000', '#F08080', '#00FA9A', '#00BFFF', '#4169E1', '#FF00FF',
                                 '#FFFACD', '#FFDAB9', '#DCDCDC', '#FFFF00'])
            for bs in self.bs_list:
                clr = next(colors)
                x = []
                y = []
                for ms in bs.connected_ms_list:
                    x.append(ms.position[0])
                    y.append(ms.position[1])
                    ax.scatter(x, y, s=9, color=clr)
        else:
            x_a = []
            y_a = []
            for ms in self.ms_list:
                x_a.append(ms.position[0])
                y_a.append(ms.position[1])
                ax.scatter(x_a, y_a, s=9, color='red')

        theta = np.linspace(0, 2 * np.pi, num=100)
        circle_x = self.grid_radius * np.cos(theta)
        circle_y = self.grid_radius * np.sin(theta)

        ax.plot(circle_x, circle_y, 'k', linewidth=0.5)

        ax.set_xlim([min(circle_x), max(circle_x)])
        ax.set_ylim([min(circle_y), max(circle_y)])

        return ax

    def initialize_random_states(self):

        num_states = len(self.parameters.state_indexes)
        random_states = []

        # Initialize each random state from seed position in set of seeds
        for index in range(0, num_states):
            state_seed = self.__seed_set[self.__seed + index]
            random_states.append(np.random.RandomState(state_seed))

        return random_states

    def reset_state(self):

        self.__seed_count += 1

        if self.__seed_count < len(self.parameters.seeds):
            # Get new seed from predetermined simulation seeds
            self.__seed = self.parameters.seeds[self.__seed_count]
            # Reinitialize all random states
            self.__random_states = self.initialize_random_states()

        # Empty lists
        self.__ms_list = []
        for bs in self.bs_list:
            bs.reset_list()

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
    def grid_radius(self):
        return self.__grid_radius

    @property
    def connected(self):
        return self.__connected
