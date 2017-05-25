# -*- coding: utf-8 -*-
"""
Main script.

Created on Mon Apr  3 20:35:22 2017

@author: Guilherme
"""

from src.main.parameters.base_station_parameters import BaseStationParameters
#from src.main.simulation_thread import SimulationThread
from src.main.topology import Topology
from src.main.base_station import BaseStation
from src.main.parameters.topology_parameters import TopologyParameters
from src.main.support.enumerations import TopologyModel
from src.main.support.graphics import *
from src.main.support.rotation import *

figs_dir = "figs/"

bs_param = BaseStationParameters()
topology_param = TopologyParameters()

hex_grid = Topology(TopologyModel.HexagonalGrid, topology_param)

base_station_list = []

# Central Station
base_station_list.append(BaseStation(200, 200, hex_grid.base_station_height, bs_param))

for layer in range(hex_grid.layer_number):
    index_1 = layer + 1
    x_position = 200-(index_1*50)
    y_position = 200
    #bs_position = Point(200-(index_1*50), 200)
    for index_2 in range(index_1 * 6):
        base_station_list.append(BaseStation(x_position, y_position, hex_grid.base_station_height, bs_param))
        bs_position = rotate((200, 200), (x_position, y_position), -math.radians(60))

window = GraphWin('System Level Simulator', 400, 400)

for index in range(len(base_station_list)):
    list_item = base_station_list[index]
    point = Point(list_item.x_position, list_item.y_position)
    window.plot(list_item.x_position, list_item.y_position)

# sim_thread = SimulationThread(param,figs_dir)
#
# sim_thread.simulate()