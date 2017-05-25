# -*- coding: utf-8 -*-
"""
Enumerations used in the project.

Created on Wed May 24 23:37:35 2017

@author: Guilherme
"""

from enum import Enum

class TopologyModel(Enum):
    """
    Types of topology
    """
    HexagonalGrid = 0

    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self.value == other.value
        return NotImplemented


