'''
Created on 5 déc. 2016

@author: olinox
'''
from pypog.geometry import line2d, zone


class BasePencil(object):
    
    def __init__(self, grid):
        self._grid = grid
        
        self._origin = None
        self._position = None
        
        self._size = 1
        self._selection = []

        self._added = []
        self._removed = []

    @property
    def origin(self):
        return self._coord0

    @origin.setter
    def origin(self, x, y):
        self._origin = (x, y)

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, size):
        if not size > 0:
            raise ValueError("size has to be strictly positive")
        self._size = size

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, x, y):
        self._position = (x, y)
        self._update()

    @property
    def selection(self):
        return self._selection
        
    @property
    def added(self):
        return self._added

    @property
    def removed(self):
        return self._removed

    def _update(self):
        pass
        
        
class LinePencil(BasePencil):
    def __init__(self, *args):
        BasePencil.__init__(*args)
        
    def _update(self):
        x0, y0 = self.origin
        x, y = self.position
        
        result = set([])
        line = line2d(self._grid.cell_shape, x0, y0, x, y)
        for x, y in line:
            result |= set( zone(self._grid.cell_shape, x, y, self.size) )
        
        self._added = list( result - self._selection )
        self._removed = list( self._selection - result ) 
        self._selection = list( result )


class SimplePencil(BasePencil):
    def __init__(self, *args):
        BasePencil.__init__(*args)
        
    def _update(self):
        x, y = self.position
        zone = zone(self._grid.cell_shape, x, y, self.size)

        self._added = list( set(zone) - set(self._selection) )
        self._selection = list( set(self._selection) + set(zone))
        
        

