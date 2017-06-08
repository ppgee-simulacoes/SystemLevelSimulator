# -*- coding: utf-8 -*-
"""
Main script.

Created on Mon Apr  3 20:35:22 2017

@author: Guilherme
"""

from src.main.base_station import BaseStation
from src.main.parameters.base_station_parameters import BaseStationParameters
from src.main.parameters.hexagonal_grid_parameters import HexagonalGridParameters
from src.main.support.enumerations import TopologyModel
from src.main.support.graphics import *
from src.main.support.rotation import *
from src.main.simulation_thread import SimulationThread
from src.main.hexagonal_grid import Hexagonal_Grid
import time
import matplotlib.pyplot as plt


figs_dir = "figs/"

bs_param = BaseStationParameters()
hexagonal_param = HexagonalGridParameters()
simulation_thread = SimulationThread()

# hex_grid = Topology(TopologyModel.HexagonalGrid, topology_param)
hex_grid = Hexagonal_Grid(TopologyModel.HexagonalGrid, hexagonal_param)


base_station_list = []

# Central Station
base_station_list.append(BaseStation(800, 800, 0, bs_param))

for layer in range(hex_grid.layer_number):
    index_1 = layer + 1
    x_position = 800-(index_1*50)
    y_position = 800
    for index_2 in range(index_1 * 6):
        base_station_list.append(BaseStation(x_position, y_position, 0, bs_param))
        x_position, y_position = rotate((800, 800), (x_position, y_position), -math.radians(60/index_1))


#print(base_station_list)

window = GraphWin('System Level Simulator', 800, 800)

for index in range(len(base_station_list)):
    list_item = base_station_list[index]
    point = Point(list_item.x_position, list_item.y_position)

    # print (point)
    # window.plot(list_item.x_position, list_item.y_position)


    plt.subplot(1, 1, 1)
    plt.plot(list_item.x_position, list_item.y_position, u'*')

plt.show()

time.sleep(10)

# sim_thread = SimulationThread(param,figs_dir)
#
# sim_thread.simulate()