'''
Created on 7 nov. 2016
    Game Grid
@author: olinox
'''
from pypog import geometry
from pypog import pathfinder


ORIGIN_HPOSITION_LEFT = 0
ORIGIN_HPOSITION_MIDDLE = 1
ORIGIN_HPOSITION_RIGHT = 2
ORIGIN_VPOSITION_TOP = 10
ORIGIN_VPOSITION_MIDDLE = 11
ORIGIN_VPOSITION_BOTTOM = 12


class Grid(object):
    def __init__(self, cell_shape, width, height, roof = None):
        self._cell_shape = None
        self.cell_shape = cell_shape
        
        self._width = 0
        self.width = width
        self._height = 0
        self.height = height
        
        self._roof = roof

        self._cells = {}
        self._build()
        
    def _build(self):
        for x in range(self.width):
            for y in range(self.height):
                cell = Cell(self.cell_shape, x, y)
                self._cells[(x, y)] = cell

    # properties
    @property
    def cell_shape(self):
        return self._cell_shape
    
    @cell_shape.setter
    def cell_shape(self, cell_shape):
        if not cell_shape in geometry.GRID_GEOMETRIES:
            raise ValueError("'cell_shape' has to be a value from GRID_GEOMETRIES")
        self._cell_shape = cell_shape
        
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
    
    @property
    def roof(self):
        return self._roof
    
    def cell(self, x, y):
        return self._cells[(x, y)]
    
    @property
    def cells(self):
        return self._cells
    
    
    # geometric methods
    def cases_number(self):
        return self.height * self.width
    
    def in_grid(self, x, y):
        """return True if the coordinates are in the grid"""
        return (x > 0 and x <= self._width and y > 0 and y <= self._height)
    
    def line(self, x1, y1, x2, y2):
        return geometry.line2d(self.cell_shape, x1, y1, x2, y2)
    
    def line3d(self, x1, y1, z1, x2, y2, z2):
        return geometry.line3d(self.cell_shape, x1, y1, z1, x2, y2, z2)
    
    def zone(self, x, y, radius):
        return geometry.zone(self.cell_shape, x, y, radius)
    
    def triangle(self, xa, ya, xh, yh, iAngle):
        return geometry.triangle(self.cell_shape, xa, ya, xh, yh, iAngle)
    
    def triangle3d(self, xa, ya, za, xh, yh, zh, iAngle):
        return geometry.triangle3d(self.cell_shape, xa, ya, za, xh, yh, zh, iAngle)

    def rect(self, x1, y1, x2, y2):
        return geometry.rect(x1, y1, x2, y2)
    
    def hollow_rect(self, x1, y1, x2, y2):
        return geometry.hollow_rect(x1, y1, x2, y2)


    # pathfinding methods
    def moving_cost(self, *args):
        return 1
    
    def path(self, x1, y1, x2, y2):
        return pathfinder.path( self, (x1, y1), (x2,y2), self.moving_cost_function )


class HexGrid(Grid):
    def __init__(self, width, height):
        Grid.__init__(self, geometry.HEX, width, height)

class SquareGrid(Grid):
    def __init__(self, width, height):
        Grid.__init__(self, geometry.SQUARE, width, height)



class Cell(object):
    def __init__(self, cell_shape, x, y, z = 0):
        self._cell_shape = cell_shape
        self._x = x
        self._y = y
        self._z = z

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

