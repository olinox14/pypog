'''
Created on 25 nov. 2016

@author: olinox
'''
from core import geometry
from core.pencil.pbase import BasePencil


class LinePencil(BasePencil):
    def __init__(self, *args):
        BasePencil.__init__(*args)
        
    def _update(self):
        x0, y0 = self.origin
        x, y = self.position
        
        result = set([])
        line = geometry.gline.line2d(self._grid.grid_shape, x0, y0, x, y)
        for x, y in line:
            result |= set( geometry.gzone.zone(self._grid.grid_shape, x, y, self.size) )
        
        self._added = list( result - self._selection )
        self._removed = list( self._selection - result ) 
        self._selection = list( result )
