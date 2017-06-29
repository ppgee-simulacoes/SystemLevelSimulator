import numpy as np

class MobileStation(object):
    """
        MobileStation is a class that creates each mobile station (MS) in the Topology grid.
        
        Properties:
            index <1x1 inf>: MS index
            position <1x3 np.array>: coordinate (x, y, z) of MS in meters
            tx_power <1x1 float>: MS transmit power in dB
            rx_power <1x1 float>: MS max received power in dB
            interference_power <1xnum_bs float list>: List of BS interference power in dB
            connected_bs <BaseStation>: base station to which MS is connected
            
        Constructor:
            Syntax: self = MobileStation(position, power, index)
            Inputs: position <1x3 float>: coordinate (x, y, z) of MS in meters
                    power <1x1 float>: MS transmit power in dB
                    index <1x1 inf>: MS index
                    
        Methods:
            connect_to:
                Gets connected BS.
                Syntax: self.connect_to(bs)
                Inputs: bs <1x1 BaseStation> BS to be connected            
                
        Author: Artur Rodrigues
                artur.rodrigues@ieee.org
                
        Version History:
            V. 0.1 (June 16 2017) - class created
    """
    
    def __init__(self, position, power, n0, tx_band, index):

        self.__index = index

        self.__position = position
        self.__tx_power = power

        self.__rx_power = None
        self.__interference_power = []

        noise_density = 10**(n0/10)
        self.__noise = 10 * np.log10(tx_band * noise_density)

        self.__connected_bs = None

    def connect_to(self, bs):
        self.__connected_bs = bs

    def calculate_snir(self):
        interference = 10**(np.asarray(self.interference_power)/10)
        noise = 10**(self.noise/10)
        snir = self.rx_power - 10*(np.log10(sum(interference) + noise))

        return snir

    @property
    def index(self):
        return self.__index

    @property
    def position(self):
        return self.__position
    
    @property
    def tx_power(self):
        return self.__tx_power

    @property
    def rx_power(self):
        return self.__rx_power

    @rx_power.setter
    def rx_power(self, rx_power):
        self.__rx_power = rx_power

    @property
    def interference_power(self):
        return self.__interference_power

    @property
    def noise(self):
        return self.__noise

    @property
    def connected_bs(self):
        return self.__connected_bs
