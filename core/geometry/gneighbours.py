'''
Created on 19 nov. 2016

@author: olinox
'''
from core import geometry


def neighbours_of(grid_shape, x, y):
    if grid_shape == geometry.SQUARE:
        return squ_neighbours_of(x, y)
    elif grid_shape == geometry.HEX: 
        return hex_neighbours_of(x, y)
    else:
        raise ValueError("'geometry' has to be a value from GRID_GEOMETRIES")

def hex_neighbours_of(x, y):
    """ returns the list of coords of the neighbours of a cell on an hexagonal grid"""
    if x%2 == 0:
        return [(x, y-1), (x+1, y-1), (x+1, y), (x,  y+1), (x-1, y), (x-1, y-1)]
    else:
        return [(x, y-1), (x+1, y), (x+1, y+1), (x,  y+1), (x-1, y+1), (x-1, y)]        

def squ_neighbours_of(x, y):
    """ returns the list of coords of the neighbours of a cell on an square grid"""
    return [(x-1, y-1), (x, y-1), (x+1, y-1), \
            (x-1, y)  , (x, y-1), (x+1, y)  , \
            (x-1, y+1), (x, y+1),(x+1, y+1)]
    
