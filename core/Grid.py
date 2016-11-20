'''
Created on 7 nov. 2016
    Game Grid
@author: olinox
'''
from core.Cell import Cell
from core.constants import GRID_GEOMETRIES
from core import geometry
from core.pathfinder import pathfinder


class Grid(object):
    def __init__(self, geometry, width, height):
        self._geometry = None
        self.geometry = geometry
        
        self._width = 0
        self.width = width
        self._height = 0
        self.height = height
        
        self._cells = {}
        
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
    
    
    
    
    def cell(self, coord):
        # temporary
        try:
            return self._cells[coord]
        except KeyError:
            x, y = coord
            cell = Cell(self._geometry, x, y)
            self._cells[coord] = cell
            return cell
    
    # methods
    def cases_number(self):
        return self.height * self.width
    
    def in_grid(self, x, y):
        """return True if the coordinates are in the grid"""
        return (x > 0 and x <= self._width and y > 0 and y <= self._height)
    
    def line(self, x1, y1, x2, y2):
        return geometry.gline.line2d(self.geometry, x1, y1, x2, y2)
    
    def line3d(self, x1, y1, z1, x2, y2, z2):
        return geometry.gline.line3d(self.geometry, x1, y1, z1, x2, y2, z2)
    
    def zone(self, x, y):
        return geometry.gzone.zone(self.geometry, x, y)
    
    def triangle(self, xa, ya, xh, yh, iAngle):
        return geometry.gtriangle.triangle(self.geometry, xa, ya, xh, yh, iAngle)
    
    def triangle3d(self, xa, ya, za, xh, yh, zh, iAngle):
        return geometry.gtriangle.triangle3d(self.geometry, xa, ya, za, xh, yh, zh, iAngle)

    def rect(self, x1, y1, x2, y2):
        return geometry.grectangle.rect(x1, y1, x2, y2)
    
    def hollow_rect(self, x1, y1, x2, y2):
        return geometry.grectangle.hollow_rect(x1, y1, x2, y2)

    def path(self, x1, y1, x2, y2):
        return pathfinder.path( self, (x1, y1), (x2,y2) )

    
    
    
    
class HexGrid(Grid):
    def __init__(self, width, height):
        Grid.__init__(self, 5, width, height)

class SquareGrid(Grid):
    def __init__(self, width, height):
        Grid.__init__(self, 4, width, height)

    