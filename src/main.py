"""
    Main Simulation Script.
    
    Author: Artur Rodrigues
            artur.rodrigues@ieee.org
                
        Version History:
            V. 0.1 (May 31 2017) - created 

"""

from parameters.parameters import Parameters
from simulation_thread import SimulationThread

param = Parameters()
sim_thread = SimulationThread(param)

sim_thread.simulate()

