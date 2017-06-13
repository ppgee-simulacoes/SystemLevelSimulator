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
    
class PropagationModel(Enum):
    """
        Possible propagation models used in the simulation
        
        Properties:
            
            GENERIC -- generic model
            FREESPACE -- free space loss model
            OKUMURA -- Okumura-Hata/COST model
    
            Author: Calil Queiroz
                calil.queiroz@ieee.org
                       
            Version History:
                V. 0.1 (Jun 13 2017) - class created   
    """
    
    GENERIC = 0
    FREESPACE = 1
    OKUMURA = 2
    
    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self.value == other.value
        return NotImplemented
    
class OkumuraEnv(Enum):
    """
        Okumura-Hata/COST environment.
        
        Properties:
            
            URBAN -- urban environment
            SUBURBAN -- suburban environment
            RURAL -- rural environment
    
            Author: Calil Queiroz
                calil.queiroz@ieee.org
                       
            Version History:
                V. 0.1 (Jun 13 2017) - class created   
    """
    
    URBAN = 0
    SUBURBAN = 1
    RURAL = 2
    
    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self.value == other.value
        return NotImplemented
    
