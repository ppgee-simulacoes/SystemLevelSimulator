import numpy as np

class BaseStation(object):
    """
        BaseStation is a class that creates each base station (BS) in the Topology grid.
        
        Properties:
            index <1x1 inf>: MS index
            position <1x3 np.array>: coordinate (x, y, z) of BS in meters 
            azimuth <1x1 float>: antenna azimuth in degrees
            tilt <1x1 float>: antenna tilt in degrees
            tx_power <1x1 float>: BS transmit power in dB
            ms_rx_power <1x1 N float list> received power of each of the N connected MSs
            interference_power <1xnum_bs float list>: list of MS interference power from each BS in dB
            connected_ms_list <1xN list>: list of N connected mobile stations
            
        Constructor:
            Syntax: self = BaseStation(position, azimuth, tilt, power, index)
            Inputs: position <1x3 float>: coordinate (x, y, z) of BS in meters
                    azimuth <1x1 float>: antenna azimuth in degrees
                    downtilt <1x1 float>: antenna downtilt in degrees
                    power <1x1 float>: BS transmit power in dB
                    index <1x1 inf>: MS index
                    
        Methods:
            connect_to:
                Gets connected MS and adds it to BSs list.
                Syntax: self.connect_to(ms)
                Inputs: ms <1x1 MobileStation> MS to be connected
            reset_list:
                Resets list of MSs for new iteration.
                Syntax: self.reset_list()
                
        Author: Artur Rodrigues
                artur.rodrigues@ieee.org
                
        Version History:
            V. 0.1 (June 16 2017) - class created
    """

    def __init__(self, position, azimuth, downtilt, power, n0, tx_band, index):

        self.__index = index

        self.__position = position
        self.__azimuth = azimuth
        self.__downtilt = downtilt
        self.__tx_power = power

        noise_density = 10**(n0/10)
        self.__noise = 10 * np.log10(tx_band * noise_density)

        self.__ms_rx_power = []

        self.__interference_power = None
        self.__connected_ms_list = []
        
    def connect_to(self, ms):
        self.__connected_ms_list.append(ms)

    def get_rx_power(self, ms_rx_power):
        self.__ms_rx_power.append(ms_rx_power)

    def calculate_antenna_gain(self, ms_position):
        # Antenna Model Kathrein 742215 based on Gunnarson et al, 2008
        # "Downtilted Base Station Antennas – A Simulation Model Proposal and
        # Impact on HSPA and LTE Performance"

        relative_position = np.array([(ms_position[0] - self.position[0]),
                                      ms_position[1] - self.position[1]])

        # Get horizontal azimuth angle
        phi_rad = np.arctan2(relative_position[1], relative_position[0])
        phi = np.rad2deg(phi_rad)
        phi -= self.azimuth

        # Get vertical tilt angle
        distance = np.sqrt(relative_position[0] ** 2 + relative_position[1] ** 2)
        theta_rad = np.arctan2((ms_position[2] - self.position[2]), distance)
        theta = np.rad2deg(theta_rad)
        theta -= self.downtilt

        # Calculate Horizontal and Vertical Gains according to antenna model
        horizontal_gain = - min(12 * ((phi/65) ** 2), 30) + 18
        vertical_gain = max(-12 * ((theta/6.2) ** 2), -18)

        antenna_gain = horizontal_gain + vertical_gain

        return antenna_gain

    def calculate_snir(self, random_state):

        # Get random active MS from list of connected MSs and choose its power as current received power
        active_ms_index = random_state.randint(0, high=len(self.connected_ms_list))
        rx_power = self.ms_rx_power[active_ms_index]

        interference = 10 ** (np.asarray(self.interference_power) / 10)
        noise = 10 ** (self.noise / 10)
        snir = rx_power - 10 * (np.log10(sum(interference) + noise))

        return snir

    def reset_list(self):
        self.__connected_ms_list = []
        self.__ms_rx_power = []

    @property
    def index(self):
        return self.__index

    @property
    def position(self):
        return self.__position

    @property
    def azimuth(self):
        return self.__azimuth

    @property
    def downtilt(self):
        return self.__downtilt

    @property
    def tx_power(self):
        return self.__tx_power

    @property
    def ms_rx_power(self):
        return self.__ms_rx_power

    @property
    def interference_power(self):
        return self.__interference_power

    @interference_power.setter
    def interference_power(self, interference_power):
        self.__interference_power = interference_power

    @property
    def noise(self):
        return self.__noise

    @property
    def connected_ms_list(self):
        return self.__connected_ms_list

