'''
Created on 8 nov. 2016
    Cell of a board game
@author: olinox
'''
from core import geometry


class Cell(object):
    def __init__(self, geometry, x, y, z = 0):
        if not all(isinstance(value, int) for value in [x, y, z]):
            raise TypeError("x, y and z should be integers")
        self._geometry = geometry
        self._x = x
        self._y = y
        self._z = z
        self._neighbours = ()
        self.__update_neighbours()

    @property
    def x(self):
        return self._x
    
    @property
    def y(self):
        return self._y
    
    @property
    def z(self):
        return self._z
    
    @property
    def coord(self):
        return (self._x, self._y)
    
    @property
    def coord3d(self):
        return (self._x, self._y, self._z)
    
    def __repr__(self):
        return "Cell {}".format(self.coord)
    
    @property
    def neighbours(self):
        return self._neighbours
    
    def __update_neighbours(self):
        """update the tuple of neighbours cells"""
        x, y = self._x, self._y
        if self._geometry == geometry.HEX:
            if 1 == (x % 2):
                self._neighbours = ( (x, y-1), (x+1, y), (x+1, y+1), (x,  y+1), (x-1, y+1), (x-1, y) )
            else:
                self._neighbours = ( (x, y-1), (x+1, y-1), (x+1, y), (x,  y+1), (x-1, y), (x-1, y-1) )
        elif self._geometry == geometry.SQUARE:
            self._neighbours = ( (x-1, y-1), (x, y-1), (x+1, y-1), \
                                (x-1, y)  , (x, y-1), (x+1, y)  , \
                                (x-1, y+1), (x, y+1),(x+1, y+1) )
    
    