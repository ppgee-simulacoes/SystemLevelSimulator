from enum import Enum


class SimType(Enum):
    """
    SimType is an enumeration class for the possible stopping criteria.
    
    
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
