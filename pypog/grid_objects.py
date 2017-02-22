'''
    Game Grid

    ** By Cro-Ki l@b, 2017 **
'''
from pypog import geometry
from pypog import pathfinding


ORIGIN_HPOSITION_LEFT = 0
ORIGIN_HPOSITION_MIDDLE = 1
ORIGIN_HPOSITION_RIGHT = 2
ORIGIN_VPOSITION_TOP = 10
ORIGIN_VPOSITION_MIDDLE = 11
ORIGIN_VPOSITION_BOTTOM = 12


class Grid(object):
    def __init__(self, cell_shape, width, height, roof=None):
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
        if not cell_shape in geometry.CELL_SHAPES:
            raise ValueError("'cell_shape' has to be a value from CELL_SHAPES")
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
        return geometry.line(self.cell_shape, x1, y1, x2, y2)

    def line3d(self, x1, y1, z1, x2, y2, z2):
        return geometry.line3d(self.cell_shape, x1, y1, z1, x2, y2, z2)

    def zone(self, x, y, radius):
        return geometry.zone(self.cell_shape, x, y, radius)

    def triangle(self, xa, ya, xh, yh, iAngle):
        return geometry.triangle(self.cell_shape, xa, ya, xh, yh, iAngle)

    def triangle3d(self, xa, ya, za, xh, yh, zh, iAngle):
        return geometry.triangle3d(self.cell_shape, xa, ya, za, xh, yh, zh, iAngle)

    def rect(self, x1, y1, x2, y2):
        return geometry.rectangle(x1, y1, x2, y2)

    def hollow_rect(self, x1, y1, x2, y2):
        return geometry.hollow_rectangle(x1, y1, x2, y2)


    # pathfinding methods
    def moving_cost(self, *args):
        return 1

    def path(self, x1, y1, x2, y2):
        return pathfinding.path(self, (x1, y1), (x2, y2), self.moving_cost_function)


class HexGrid(Grid):
    def __init__(self, width, height):
        Grid.__init__(self, geometry.FLAT_HEX, width, height)

class SquareGrid(Grid):
    def __init__(self, width, height):
        Grid.__init__(self, geometry.SQUARE, width, height)



class Cell(object):
    def __init__(self, cell_shape, x, y, z=0):
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


class Piece(object):
    def __init__(self):
        super(Piece, self).__init__()
        self._position = ()
        self._rotation = 0
        self._height = 1
        self._zR = 0
        self._cell_shape = None
        self._shape = [ (0, 0) ]

    # properties
    @property
    def position(self):
        """return the (x, y) position of the Piece"""
        return self._position

    @position.setter
    def position(self, position):
        """update the (x, y) position of the Piece
        x, y have to be integers"""
        try:
            _, _ = position
            if not all([isinstance(var, int) for var in position]):
                raise ValueError("'position' have to be an (x, y) tuple, with x and y integers")
        except ValueError:
            raise ValueError("'position' have to be an (x, y) tuple, with x and y integers")
        self._position = position

    @property
    def x(self):
        """x coordinate of the Piece"""
        return self._position[0]

    @property
    def y(self):
        """y coordinate of the Piece"""
        return self._position[1]

    @property
    def height(self):
        """height (in cells) of the Piece"""
        return self._height

    @height.setter
    def height(self, height):
        """set the height (in cells) of the Piece
        'height' has to be a positive integer"""
        if not isinstance(height, int):
            raise TypeError("'height' has to be an integer")
        if not height >= 0:
            raise TypeError("'height' has to be positive")
        self._height = height

    @property
    def zR(self):
        """return the relative altitude of the Piece
        the relative altitude is the difference of altitude between the bottom of the Piece
        and the altitude of its position"""
        return self._zR

    @zR.setter
    def zR(self, zR):
        """set the relative altitude of the Piece"""
        if not isinstance(zR, int):
            raise TypeError("'zR' has to be an integer")
        self._zR = zR

    @property
    def shape(self):
        """return the shape of the Piece
        shape is a list of relative coordinates, assuming (0, 0) is the position of the piece
        eg: [(-1, -1), (-1, 0), (0, 0)]"""
        return self._shape

    @shape.setter
    def shape(self, shape):
        """set the shape of the piece (see shape property for more informations)"""
        if not isinstance(shape, list):
            raise TypeError("'shape' has to be a list")
        for item in shape:
            try:
                _, _ = item
                if not all([isinstance(var, int) for var in item]):
                    raise ValueError("'shape' have to be a list of (x, y) tuples, with x and y integers")
            except ValueError:
                raise ValueError("'shape' have to be a list of (x, y) tuples, with x and y integers")
        self._shape = shape

    @property
    def cell_shape(self):
        """return the 'cell_shape' from GRID_GEOMETRIES for which the Piece is made for.
        Cell's shape is needed for pivot algorithm, and for graphical purposes"""
        return self._cell_shape

    @cell_shape.setter
    def cell_shape(self, cell_shape):
        """set the 'cell_shape' of the piece (see cell_shape property for more informations)"""
        self._cell_shape = cell_shape

    @property
    def rotation(self):
        """return the current rotation of the piece.
        rotation is an integer representing the number of pivot applied to the piece"""
        return self._rotation

    @rotation.setter
    def rotation(self, rotation):
        """set the 'rotation' of the piece (see rotation property for more informations)"""
        if not isinstance(rotation, int):
            raise TypeError("'rotation' has to be an integer")
        self._rotation = rotation

    # methods
    def occupation(self):
        """return the list of the (x, y) coordinates currently occupied by the Piece"""
        result = [ (xr + self.x, yr + self.y) for xr, yr in self._shape ]
        if self._rotation != 0:
            result = geometry.pivot(self._cell_shape, self.position, result, self.rotation)
        return result

    def occupation3d(self, dz=0):
        """return the list of the (x, y, z) coordinates currently occupied by the Piece

        Because Pieces altitude zR is relative, the z coordinate returned is not an absolute altitude
        If you want an absolute altitude, use the 'dz' modifier to correct the result."""
        occupation = self.occupation()
        return [(x, y, z) for x, y in occupation for z in range(dz + self.zR, dz + self.zR + self.height)]

    def move_to(self, x, y, zR=None):
        """move the piece to (x, y) position and is requested to zR relative altitude"""
        self.position = x, y
        if zR != None:
            self.zR = zR

    def rotate(self, i):
        """pivot the Piece i times (counterclockwise rotation, i can be negative)"""
        new_rotation = self.rotation + i
        self.rotation = new_rotation % self.cell_shape


