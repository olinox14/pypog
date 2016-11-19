'''
Created on 19 nov. 2016

@author: olinox
'''
from core.geometry import neighbours


def zone(geometry, x0, y0, radius):
    """ returns the list of the coordinates of the cells in the zone around (x0, y0)
    """
    buffer = frozenset( [ (x0, y0) ] )
        
    for _ in range(0, radius):
        current = buffer
        for x, y in current:
            buffer |= frozenset( neighbours.neighbours_of( geometry, x, y ) )

    return list(buffer)
