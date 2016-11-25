'''
Created on 25 nov. 2016

@author: olinox
'''
from core import geometry
from core.pencil.pbase import BasePencil


class SimplePencil(BasePencil):
    def __init__(self, *args):
        BasePencil.__init__(*args)
        
    def _update(self):
        x, y = self.position
        zone = geometry.gzone.zone(self._grid.grid_shape, x, y, self.size)

        self._added = list( set(zone) - set(self._selection) )
        self._selection = list( set(self._selection) + set(zone))