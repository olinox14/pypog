'''
Created on 6 mars 2017

@author: olinox
'''

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
