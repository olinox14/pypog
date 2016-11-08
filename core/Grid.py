'''
Created on 7 nov. 2016
    Game Grid
@author: olinox
'''
from core import bresenham, triangle, rectangle
from core.constants import GRID_GEOMETRIES
from core.triangle import ANGLES


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
    
    def in_grid(self, x, y):
        """return True if the coordinates are in the grid"""
        return (x > 0 and x <= self._width and y > 0 and y <= self._height)
    
    def line(self, x1, y1, x2, y2):
        return bresenham.line2d(self.geometry, x1, y1, x2, y2)
    
    def line3d(self, x1, y1, z1, x2, y2, z2):
        return bresenham.line3d(self.geometry, x1, y1, z1, x2, y2, z2)
    
    def triangle(self, xa, ya, xh, yh, iAngle):
        return triangle.triangle(self.geometry, xa, ya, xh, yh, iAngle)
    
    def triangle3d(self, xa, ya, za, xh, yh, zh, iAngle):
        return triangle.triangle3d(self.geometry, xa, ya, za, xh, yh, zh, iAngle)

    def rect(self, x1, y1, x2, y2):
        return rectangle.rect(x1, y1, x2, y2)
    
    def hollow_rect(self, x1, y1, x2, y2):
        return rectangle.hollow_rect(x1, y1, x2, y2)


    
if __name__ == '__main__':
    gr = Grid(5, 100, 100)
    print(gr.cases_number())
    
    print(gr.line(1,1,5,10))
    print(gr.line3d(1,1,1,5,10,10))
    
    print(gr.triangle(1,1,5,10,ANGLES[1]))
    print(gr.triangle3d(1,1,1,5,10,10, ANGLES[1]))
    
    
    
    
    
    
    