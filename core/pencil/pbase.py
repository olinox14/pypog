'''
Created on 25 nov. 2016

@author: olinox
'''

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
        
