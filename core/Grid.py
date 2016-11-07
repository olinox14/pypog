'''
Created on 7 nov. 2016
    Game Grid
@author: olinox
'''
from core import bresenham
from core.constants import GRID_GEOMETRIES


class Grid(object):
    def __init__(self, geometry, width, height):
        self._geometry = geometry
        self._width = width
        self._height = height
        
    # properties
    @property
    def geometry(self):
        return self._geometry
    
    @geometry.setter
    def geometry(self, geometry):
        if not geometry in GRID_GEOMETRIES:
            raise ValueError("'geometry' has to be a value from GRID_GEOMETRIES")
        self._geometry = geometry
        
    @property
    def width(self):
        return self._width
    
    @width.setter
    def width(self, width):
        if not isinstance(width, int) or not width > 0:
            raise ValueError("'width' has to be a strictly positive integer")
        self._width = width
        
    @property
    def height(self):
        return self._height
    
    @height.setter
    def height(self, height):
        if not isinstance(height, int) or not height > 0:
            raise ValueError("'width' has to be a strictly positive integer")
        self._height = height    
    
    # methods
    def cases_number(self):
        return self.height * self.width
    
    def line(self, *args):
        if len(args) == 4:
            x1, y1, x2, y2 = args
            return bresenham.line2d(self.geometry, x1, y1, x2, y2)
        if len(args) == 6:
            x1, y1, z1, x2, y2, z2 = args
            return bresenham.line3d(self.geometry, x1, y1, z1, x2, y2, z2)
    
    
    
    
if __name__ == '__main__':
    gr = Grid(5, 100, 100)
    print(gr.cases_number())
    print(gr.line(1,1,5,10))
    print(gr.line(1,1,1,5,10,10))
    
    
    
    
    
    
    