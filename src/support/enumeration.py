from enum import Enum


class SimType(Enum):
    """
        SimType is an enumeration class to define the possible types of simulation loop, 
        according to determined stopping criteria.
    
        Properties:
            FIXED_SEEDS -- Simulate for given seeds and calculate confidence 
                        interval
            FIXED_CONF  -- Simulate multiple seeds util a confidence interval is
                        reached
                       
            Author: Artur Rodrigues
                artur.rodrigues@ieee.org
                       
            Version History:
                V. 0.1 (May 31 2017) - class created 
    """
    FIXED_SEEDS = 0
    FIXED_CONF = 1

    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self.value == other.value
        return NotImplemented


class RandomSeeds(Enum):
    """
        RandomSeeds is an enumeration class to define the random streams constants.
        
        Properties:
            
            MOBILE_POSITION -- mobile random position
    
            Author: Artur Rodrigues
                artur.rodrigues@ieee.org
                       
            Version History:
                V. 0.1 (May 31 2017) - class created   
    """

    MOBILE_POSITION = 0

    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self.value == other.value
        return NotImplemented
