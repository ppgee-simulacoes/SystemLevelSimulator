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
            SHADOWING - fading due to shadowing
            ACTIVE_MOBILE -- active mobile index in each BS list
    
            Author: Artur Rodrigues
                artur.rodrigues@ieee.org
                       
            Version History:
                V. 0.1 (May 31 2017) - class created   
    """

    MOBILE_POSITION = 0
    SHADOWING = 1
    ACTIVE_MOBILE = 2

    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self.value == other.value
        return NotImplemented


class PropagationModel(Enum):
    """
        PropagationModel is an enumeration class to define the possible types of propagation scenarios.

        Properties:

            GENERIC -- Generic Log Normal Path Loss Model
            FREE_SPACE -- Free Space Propagation Model
            OKUMURA_COST -- Okumura-Hata/Cost 231 based Empiric Model

            Author: Artur Rodrigues
                artur.rodrigues@ieee.org

            Version History:
                V. 0.1 (June 12 2017) - class created   
    """

    GENERIC = 0
    FREE_SPACE = 1
    OKUMURA_COST = 2

    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self.value == other.value
        return NotImplemented


class PropagationEnvironment(Enum):
    """
        PropagationEnvironment is an enumeration class to define the possible propagation environments for
        the Okumura-Hata/Cost 231 based Empiric Model.

        Properties:

            DENSE_URBAN -- Dense Urban Areas
            URBAN -- Medium Cities and Urban Areas
            SUBURBAN -- Suburban Areas
            RURAL -- Rural Areas

            Author: Artur Rodrigues
                artur.rodrigues@ieee.org

            Version History:
                V. 0.1 (June 12 2017) - class created
    """

    DENSE_URBAN = 0
    URBAN = 1
    SUBURBAN = 2
    RURAL = 3

    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self.value == other.value
        return NotImplemented