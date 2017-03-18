'''
    Grid objects

    ** By Cro-Ki l@b, 2017 **
'''
from pypog.geometry_objects import BaseGeometry, FHexGeometry, SquareGeometry, \
    BoundingRect, HexGeometry
from pypog.pathfinding import Pathfinder


class BaseGrid(object):
    """ Base class for grids
    This class should be overriden """
    geometry = BaseGeometry

    def __init__(self, width, height):
        """ instanciate a new BaseGrid object """
        self._width = 0
        self.width = width
        self._height = 0
        self.height = height

    def __repr__(self):
        return "<{} object>".format(self.__class__.__name__)

    @staticmethod
    def from_geometry(geometry, *args):
        if geometry == SquareGeometry:
            return SquareGrid(*args)
        elif geometry == FHexGeometry:
            return FHexGrid(*args)
        else:
            raise TypeError("geometry has to be a non-abstract subclass of BaseGeometry")

    # properties
    @property
    def width(self):
        """ the width of the grid """
        return self._width

    @width.setter
    def width(self, width):
        """ set a new width for the grid.
        the new width has to be a strictly positive integer"""
        if not isinstance(width, int) or not width > 0:
            raise ValueError("'width' has to be a strictly positive integer")
        self._width = width

    @property
    def height(self):
        """ the height of the grid """
        return self._height

    @height.setter
    def height(self, height):
        """ set a new height for the grid.
        the new height has to be a strictly positive integer"""
        if not isinstance(height, int) or not height > 0:
            raise ValueError("'width' has to be a strictly positive integer")
        self._height = height

    @property
    def br(self):
        """ return the bounding rectangle of the current Grid """
        return BoundingRect(0, 0, self.width - 1, self.height - 1)

    # geometric methods
    def __len__(self):
        """ return the number of cells in the grid """
        return self.height * self.width

    def __contains__(self, key):
        """return True if the (x, y) coordinates are in the grid"""
        try:
            self.geometry.assertCoordinates(key)
        except ValueError:
            return False
        else:
            return 0 <= key[0] < self._width and 0 <= key[1] < self._height

    def __iter__(self):
        """ iterate over the coordinates of the grid """
        for item in ((x, y) for x in range(self.width) for y in range(self.height)):
            yield item

    def __getitem__(self, index):
        """ get the coordinates at the given index """
        if not (-1 * len(self)) < index < len(self):
            raise IndexError("index is out of the grid's range (given: {})".format(index))
        if index < 0:
            index += len(self)
        y = index // self.width
        x = index % self.width
        return x, y

    # geometrical algorithms
    def neighbors(self, *args):
        return self.geometry.neighbors(*args, br=self.br)

    def line(self, *args):
        return self.geometry.line(*args, br=self.br)

    def line3d(self, *args):
        return self.geometry.line3d(*args, br=self.br)

    def zone(self, *args):
        return self.geometry.zone(*args, br=self.br)

    def triangle(self, *args):
        return self.geometry.triangle(*args, br=self.br)

    def triangle3d(self, *args):
        return self.geometry.triangle3d(*args, br=self.br)

    def rectangle(self, *args):
        return self.geometry.rectangle(*args, br=self.br)

    def hollow_rectangle(self, *args):
        return self.geometry.hollow_rectangle(*args, br=self.br)

    def rotate(self, *args):
        return self.geometry.rotate(*args, br=self.br)

    # painting
    def _compare_cells(self, x1, y1, x2, y2):
        return True

    # pathfinding
    def movingcost(self, from_x, from_y, to_x, to_y):
        return 1

    def path(self, from_x, from_y, to_x, to_y):
        return Pathfinder.a_star(self, (from_x, from_y), (to_x, to_y))

class SquareGrid(BaseGrid):
    """ Square grid object """
    geometry = SquareGeometry
    def __init__(self, *args, **kwargs):
        BaseGrid.__init__(self, *args, **kwargs)

class HexGrid(BaseGrid):
    """ Base class for hexagonal grid objects """
    geometry = HexGeometry

class FHexGrid(HexGrid):
    """ Flat-hexagonal grid object """
    geometry = FHexGeometry
    def __init__(self, *args, **kwargs):
        HexGrid.__init__(self, *args, **kwargs)
