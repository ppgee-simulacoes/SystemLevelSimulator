import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection


class Topology(object):
    """
        Topology is a class that creates the cell grid and sets all Base Station coordinates.
        
        Properties:
            cell_radius <1x1 float>: cell radius in meters
            cell_side <1x1 float>: cell side length in meters
            num_layers <1x1 int>: number of grid layers
            num_cells <1x1 int>: number of cells in the grid
            xy_coordinates <1xnum_cells list>: list of tuples for (x, y) coordinates for each BS
            bs_height <1x1 float>: height of each BS in the grid
            bs_coordinates <1xnum_cells list>: list of arrays for BSs (x, y, z) coordinates 
            
        Constructor:
            Syntax: self = Topology(cell_radius, num_layers, cell_height)
            Inputs: cell_radius <1x1 float>: cell radius in meters
                    num_layers <1x1 int>: number of grid layers
                    bs_height <1x1 float>: height of each BS in the grid
                    
        Methods:
            set_bs_positions:
                Sets all BSs positions according to hexagonal topology
                Syntax: bs_list = self.set_bs_positions()
                Outputs: bs_coordinates <1xnum_cells list>: list of arrays for BSs (x, y, z) coordinates
                         num_cells <1x1 int>: number of cells in the grid
            
            plot_topology:
                Plots the cells grid and the (x,y) positions of each BS
                Syntax: self.plot_topology()
                       
                
        Author: Calil Queiroz
                calil_queiroz@hotmail.com
                Artur Rodrigues
                artur.rodrigues@ieee.org
                
        Version History:
            V. 0.1 (May 18 2017) - created class
            V. 0.2 (June 16 2017) - class optimized
    """
    
    def __init__(self, cell_radius, num_layers, bs_height):
        
        self.__cell_radius = cell_radius
        # Get cell side length for hexagonal grid
        self.__cell_side = self.cell_radius * np.sin(np.deg2rad(60))

        self.__num_layers = num_layers
        self.__num_cells = 0

        self.__xy_coordinates = []
        self.__bs_height = bs_height
        self.__bs_coordinates = []

    def set_bs_positions(self):

        if len(self.bs_coordinates) == 0:

            # Get number of rows in the grid and row indexes
            num_rows = 2 * self.num_layers + 1
            row_indexes = np.arange(self.num_layers, -self.num_layers - 1, -1)
            # Get number of cells of each row
            num_cells_per_row = num_rows - np.abs(row_indexes)
            self.__num_cells = sum(num_cells_per_row)

            # Get (x, y) distribution in grid
            xy_positions = []
            for index, row_range in enumerate(num_cells_per_row - 1):
                x_row = list(range(-row_range, row_range + 1, 2))
                y_row = [row_indexes[index]] * num_cells_per_row[index]
                xy_positions += list(zip(x_row, y_row))

            for cell in range(0, self.num_cells):
                x, y = xy_positions[cell]
                bs_position = np.array([x * self.cell_side,
                                        y * (1.5 * self.cell_radius),
                                        self.__bs_height])
                xy = x * self.cell_side, y * (1.5 * self.cell_radius)
                self.xy_coordinates.append(xy)
                self.bs_coordinates.append(bs_position)

        return self.num_cells, self.bs_coordinates

    def plot_topology(self):
        
        fig = plt.figure(figsize=(6, 6))
        ax = fig.add_subplot(111)
        
        patches = []
        hex_coord = np.array([[self.cell_side, self.cell_radius/2],
                              [0.0, self.cell_radius],
                              [-self.cell_side, self.cell_radius/2],
                              [-self.cell_side, -self.cell_radius/2],
                              [0.0, -self.cell_radius],
                              [self.cell_side, -self.cell_radius/2]])

        for cell in range(self.num_cells):
            hx = np.copy(hex_coord)
            x, y = self.xy_coordinates[cell]
            hx[:, 0] = hx[:, 0] + x
            hx[:, 1] = hx[:, 1] + y
            poly = Polygon(hx, True)
            patches.append(poly)
        
        p = PatchCollection(patches, cmap='Greys', alpha=1.0, edgecolors='#000000')
        colors = np.zeros(len(patches))
        p.set_array(np.array(colors))
        
        ax.add_collection(p)

        list_x, list_y = zip(*self.xy_coordinates)
        ax.scatter(list_x, list_y, color='k')
        
        ax.set_xlabel("x axis [meters]")
        ax.set_ylabel("y axis [meters]")
        ax.set_xlim([np.min(list_x)-self.cell_side, np.max(list_x)+self.cell_side])
        ax.set_ylim([np.min(list_y)-self.cell_radius, np.max(list_y)+self.cell_radius])
        ax.xaxis.grid(True)
        ax.yaxis.grid(True)
        #plt.show()
        return ax
    
    @property
    def cell_radius(self):
        return self.__cell_radius

    @property
    def cell_side(self):
        return self.__cell_side
    
    @property
    def num_layers(self):
        return self.__num_layers

    @property
    def num_cells(self):
        return self.__num_cells

    @property
    def xy_coordinates(self):
        return self.__xy_coordinates

    @property
    def bs_height(self):
        return self.__bs_height

    @property
    def bs_coordinates(self):
        return self.__bs_coordinates
