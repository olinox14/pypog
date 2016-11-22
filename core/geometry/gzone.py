'''
Created on 19 nov. 2016

@author: olinox
'''
from core.geometry import gneighbours


def zone(grid_shape, x0, y0, radius):
    """ returns the list of the coordinates of the cells in the zone around (x0, y0)
    """
    if not all(isinstance(c, int) for c in [x0, y0, radius]):
        raise TypeError("x0, y0, radius have to be integers")
    if not radius >= 0:
        raise ValueError("radius has to be positive")
    buffer = frozenset( [ (x0, y0) ] )

    for _ in range(0, radius):
        current = buffer
        for x, y in current:
            buffer |= frozenset( gneighbours.neighbours_of( grid_shape, x, y ) )

    return list(buffer)
