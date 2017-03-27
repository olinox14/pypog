'''
    Geometry objects

    ** By Cro-Ki l@b, 2017 **
'''
from math import sqrt, inf

class BoundingRect(tuple):
    """ Bounding rectangle defined by a top-left (xmin, ymin) point
     and a bottom-right (xmax, ymax) point """
    def __new__(cls, xmin=-inf, ymin=-inf, xmax=inf, ymax=inf):
        return tuple.__new__(cls, (xmin, ymin, xmax, ymax))

    @classmethod
    def from_(cls, *args):
        BaseGeometry.assertCoordinates(*args)
        xs, ys = zip(*list(args))
        xs, ys = sorted(list(xs)), sorted(list(ys))
        return cls(xs[0], ys[0], xs[-1], ys[-1])

    @property
    def xmin(self):
        return self[0]

    @property
    def ymin(self):
        return self[1]

    @property
    def xmax(self):
        return self[2]

    @property
    def ymax(self):
        return self[3]

    def __contains__(self, key):
        BaseGeometry.assertCoordinates(key)
        return self.xmin <= key[0] <= self.xmax and self.ymin <= key[1] <= self.ymax

    @property
    def topleft(self):
        return (self.xmin, self.ymin)

    @property
    def bottomright(self):
        return (self.xmax, self.ymax)

    @property
    def width(self):
        return self.xmax - self.xmin + 1

    @property
    def height(self):
        return self.ymax - self.ymin + 1

class BaseGeometry:
    """ Base class for geometry classes
    ! Should be overriden """
    ANGLES = (1, 2, 3)

    def __repr__(self):
        return "<{} object>".format(self.__class__.__name__)

    @classmethod
    def instance(cls):
        return cls()

    @staticmethod
    def assertCoordinates(*args):
        """ raise a ValueError if the args are not (x, y) iterables, where x and y are integers
        usage:
            self.assertCoordinates((x1, y1), (x2, y2), ...)
        """
        try:
            if all([isinstance(i, int) for x, y in args for i in (x, y)]):
                return
        except (TypeError, ValueError):
            pass
        raise ValueError("'{}' is not a valid (x, y) coordinates iterable".format(args))

    @staticmethod
    def _assertPositiveInt(value, strict=False):
        """ raise a ValueError if the 'value' is not a dimension,
        i.e. a (strictly) positive integer """
        if not isinstance(value, int) or not ((value > 0) or (not strict and value >= 0)):
            raise ValueError("Expected: strictly positive integer(given: '{}')".format(value))

    @staticmethod
    def _assertValidAngle(value):
        """ raise a ValueError if the 'value' is not a valid angle """
        if not value in BaseGeometry.ANGLES:
            raise ValueError("angle has to be a value from BaseGeometry.ANGLES (given: {})".format(value))

    @staticmethod
    def _bounding_rect(*args):
        """ return the bounding rectangle of the from (x, y) coordinates """
        return BoundingRect.from_(*args)

    @staticmethod
    def graphicsitem(x, y, scale=120):
        """ returns the list of the points which compose the (x, y) cell """
        raise NotImplementedError("this method is abstract and should be reimplemented in subclasses")

    # geometrical algorithms
    @classmethod
    def neighbors(cls, x, y, br=BoundingRect()):
        """ returns a list of the neighbors of (x, y) """
        raise NotImplementedError("this method is abstract and should be reimplemented in subclasses")

    @classmethod
    def line(cls, x1, y1, x2, y2, br=BoundingRect()):
        raise NotImplementedError("this method is abstract and should be reimplemented in subclasses")

    @classmethod
    def line3d(cls, x1, y1, z1, x2, y2, z2, br=BoundingRect()):
        """ returns a line from (x1 ,y1, z1) to (x2, y2, z2)
        as a list of (x, y, z) coordinates """
        cls.assertCoordinates((z1, z2))
        hoLine = cls.line(x1, y1, x2, y2)
        if z1 == z2:
            return [(x, y, z1) for x, y in hoLine]
        else:
            ligneZ = SquareGeometry.line(0, z1, (len(hoLine) - 1), z2)
            return [(hoLine[d][0], hoLine[d][1], z) for d, z in ligneZ]

    @classmethod
    def zone(cls, x, y, radius, br=BoundingRect()):
        """ returns the list of the coordinates of the cells in a zone around (x, y)
        """
        cls.assertCoordinates((x, y))
        cls._assertPositiveInt(radius)

        buffer = frozenset([(x, y)])

        for _ in range(0, radius):
            current = buffer
            for x, y in current:
                buffer |= frozenset(cls.neighbors(x, y))
        return list(buffer)

    @classmethod
    def triangle(cls, xa, ya, xh, yh, iAngle, br=BoundingRect()):
        """ return the list of the (x, y) coordinates in a triangle
        with (xa, ya) apex and (xh, yh) middle of the base """
        raise NotImplementedError("this method is abstract and should be reimplemented in subclasses")

    @classmethod
    def triangle3d(self, xa, ya, za, xh, yh, zh, iAngle, br=BoundingRect()):
        """Returns a list of (x, y, z) coordinates in a 3d-cone
        A is the top of the cone, H if the center of the base

        WARNING: result is a dictionary of the form {(x, y): (-z, +z)}

        This is for performance reason and because on a 2d grid, you generally don't need a complete list of z coordinates
        as you don't want to display them: you just want to know if an altitude is inside a range.

        That could change in later version
        """
        raise NotImplementedError("this method is abstract and should be reimplemented in subclasses")

    @classmethod
    def rectangle(cls, x1, y1, x2, y2, br=BoundingRect()):
        """return a list of cells in a rectangle between (X1, Y1), (X2, Y2)"""
        xmin, ymin, xmax, ymax = cls._bounding_rect((x1, y1), (x2, y2))
        return [(x, y) for x in range(xmin, xmax + 1) for y in range(ymin, ymax + 1)]

    @classmethod
    def hollow_rectangle(cls, x1, y1, x2, y2, br=BoundingRect()):
        """return a list of cells composing the sides of the rectangle between (X1, Y1), (X2, Y2)"""
        xmin, ymin, xmax, ymax = cls._bounding_rect((x1, y1), (x2, y2))
        if (xmin, ymin) == (xmax, ymax):
            return [(xmin, ymin)]
        return [(x, ymin) for x in range(xmin, xmax)] + \
               [(xmax, y) for y in range(ymin, ymax)] + \
               [(x, ymax) for x in range(xmax, xmin, -1)] + \
               [(xmin, y) for y in range(ymax, ymin, -1)]

    @classmethod
    def rotate(cls, center, coordinates, rotations, br=BoundingRect()):
        """ return the 'coordinates' list of (x, y) coordinates
        after a rotation of 'rotations' times around the (x, y) center """
        raise NotImplementedError("this method is abstract and should be reimplemented in subclasses")

    @staticmethod
    def square_distance(x1, y1, x2, y2):
        """ distance between 1 and 2 (run faster than a standard distance) """
        return (x1 - x2) ** 2 + (y1 - y2) ** 2

    @staticmethod
    def manhattan(xa, ya, xb, yb):
        """returns the manhattan distance between the two cells"""
        raise NotImplementedError("this method is abstract and should be reimplemented in subclasses")

class SquareGeometry(BaseGeometry):
    """ Geometry on square grids """
    _nodiags = False

    @staticmethod
    def graphicsitem(x, y, scale=120):
        """ reimplemented from BaseGeometry.graphicsitem """
        return  [
                    (x * scale, y * scale), \
                    ((x + 1) * scale, y * scale), \
                    ((x + 1) * scale, (y + 1) * scale), \
                    (x * scale, (y + 1) * scale)
                ]

    @classmethod
    def set_no_diags(cls, active):
        """ if nodiags is set to True, the neighbors method
        won't return the diagonals cells """
        cls._nodiags = active

    @classmethod
    def neighbors(cls, x, y, br=BoundingRect()):
        """ reimplemented from BaseGeometry._neighbors """
        cls.assertCoordinates((x, y))

        if cls._nodiags:
            return [(x, y - 1), \
                    (x - 1, y), (x + 1, y)  , \
                    (x, y + 1)]
        else:
            return [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1), \
                    (x - 1, y), (x + 1, y)  , \
                    (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)]

    @classmethod
    def line(cls, x1, y1, x2, y2, br=BoundingRect()):
        """ reimplemented from BaseGeometry.line
        Implementation of bresenham's algorithm
        """
        # check the arguments
        cls.assertCoordinates((x1, y1), (x2, y2))

        # special case
        if (x1, y1) == (x2, y2):
            return [(x1, y1)]

        # diagonal symmetry
        vertically_oriented = (abs(y2 - y1) > abs(x2 - x1))
        if vertically_oriented:
            y1, x1, y2, x2 = x1, y1, x2, y2

        # horizontal symmetry
        reversed_sym = (x1 > x2)
        if reversed_sym:
            x2, y2, x1, y1 = x1, y1, x2, y2

        # angle
        dx, dy = x2 - x1, y2 - y1
        alpha = (abs(dy) / dx)

        offset = 0.0
        step = 1 if dy > 0 else -1

        result = []
        y = y1
        for x in range(x1, x2 + 1):
            if vertically_oriented:
                result.append((y, x))
            else:
                result.append((x, y))

            offset += alpha
            if offset > 0.5:
                y += step
                offset -= 1.0

        if reversed_sym:
            result.reverse()
        return result

    @classmethod
    def triangle(cls, xa, ya, xh, yh, iAngle, br=BoundingRect()):
        """ reimplemented from BaseGeometry.triangle """
        cls.assertCoordinates((xa, ya), (xh, yh))
        cls._assertValidAngle(iAngle)

        if (xa, ya) == (xh, yh):
            return [(xa, ya)]

        result = []

        # direction vector
        dx_dir, dy_dir = xh - xa, yh - ya

        # normal vector
        dx_n, dy_n = -dy_dir, dx_dir

        # B and C positions
        k = 1 / (iAngle * sqrt(3))
        xb, yb = xh + (k * dx_n), yh + (k * dy_n)
        xc, yc = xh + (-k * dx_n), yh + (-k * dy_n)

        xb, yb = round(xb), round(yb)
        xc, yc = round(xc), round(yc)

        # sides:
        lines = [(xa, ya, xb, yb), (xb, yb, xc, yc), (xc, yc, xa, ya)]

        # base (lower slope)
        x1, y1, x2, y2 = min(lines, key=lambda x: (abs ((x[3] - x[1]) / (x[2] - x[0])) if x[2] != x[0] else 10 ** 10))
        base = cls.line(x1, y1, x2, y2)
        y_base = y1
        lines.remove((x1, y1, x2, y2))

        # 'hat' (2 other sides)
        hat = []
        y_top = None
        for x1, y1, x2, y2 in lines:
            if y_top == None:
                y_top = y2
            hat.extend(cls.line(x1, y1, x2, y2))

        # sense (1 if top is under base, -1 if not)
        sense = 1 if y_top > y_base else -1

        # rove over y values from base to hat
        for x, y in base:
            while not (x, y) in hat:
                result.append((x, y))
                y += sense
        result.extend(hat)

        return result

    @classmethod
    def triangle3d(cls, xa, ya, za, xh, yh, zh, iAngle, br=BoundingRect()):
        """ reimplemented from BaseGeometry.triangle3d """
        cls.assertCoordinates((za, zh))
        flat_triangle = cls.triangle(xa, ya, xh, yh, iAngle)

        result = {}
        k = 1 / (iAngle * sqrt(3))

        length = max(abs(xh - xa), abs(yh - ya))

        vertical_line = cls.line(0, za, length, zh)

        # build a dict with X key and value is a list of Z values
        vertical_line_dict = {d:[] for d, z in vertical_line}
        for d, z in vertical_line:
            vertical_line_dict[d].append(z)

        # this is approximative: height is update according to the manhattan distance to center
        for x, y in flat_triangle:
            distance = int(max(abs(x - xa), abs(y - ya)))
            try:
                z_list = vertical_line_dict[ distance ]
            except KeyError:
                distance = length
                z_list = vertical_line_dict[ distance ]
            dh = int(k * distance) + 1 if distance > 0 else 0
            result[ (x, y) ] = ((min(z_list) - dh) , (max(z_list) + dh))
        return result


    @classmethod
    def rotate(cls, center, coordinates, rotations, br=BoundingRect()):
        """ reimplemented from BaseGeometry.rotate """
        cls.assertCoordinates(center, *coordinates)

        if coordinates == [center] or rotations % 4 == 0:
            return coordinates
        x0, y0 = center
        result = []
        for x, y in coordinates:
            dx, dy = x - x0, y - y0
            for _ in range(rotations):
                dx, dy = dy, -dx
            xr, yr = dx + x0, dy + y0
            result.append((xr, yr))
        return result

    @staticmethod
    def manhattan(xa, ya, xb, yb):
        """ reimplemented from BaseGeometry.manhattan """
        return abs(xa - xb) + abs(ya - yb)

class HexGeometry(BaseGeometry):
    """ Base class for hexagonal grids classes
    This class should be overridden """

    @staticmethod
    def from_cubic(xu, yu, zu):
        """convert cubic coordinates (xu, yu, zu) in standards coordinates (x, y) [offset]"""
        return (zu, int(xu + (zu - (zu & 1)) / 2))

    @staticmethod
    def to_cubic(x, y):
        """converts standards coordinates (x, y) [offset] in cubic coordinates (xu, yu, zu)"""
        zu = x
        xu = int(y - (x - (x & 1)) / 2)
        yu = int(-xu - zu)
        return (xu, yu, zu)

    @staticmethod
    def cube_round(x, y, z):
        """returns the nearest (xu, yu, zu) position in cubic coordinates
        (x, y, z can be floating numbers)"""
        rx, ry, rz = round(x), round(y), round(z)
        x_diff, y_diff, z_diff = abs(rx - x), abs(ry - y), abs(rz - z)
        if x_diff > y_diff and x_diff > z_diff:
            rx = -ry - rz
        elif y_diff > z_diff:
            ry = -rx - rz
        else:
            rz = -rx - ry
        return (rx, ry, rz)

    @staticmethod
    def manhattan(*args):
        """ reimplemented from BaseGeometry.manhattan,
        using cubic coordinates"""
        try:
            xa, ya, za, xb, yb, zb = args
            return abs(xa - xb) + abs(ya - yb) + abs(za - zb)
        except ValueError:
            xa, ya, xb, yb = args
            return HexGeometry.manhattan(*HexGeometry.to_cubic(xa, ya), *HexGeometry.to_cubic(xb, yb))

class FHexGeometry(HexGeometry):
    """ Flat-hexagonal grid object """

    @staticmethod
    def graphicsitem(x, y, scale=120):
        """ reimplemented from BaseGeometry.graphicsitem """
        if x % 2 != 0:
            y += 0.5
        return [
                   (((x * 0.866) + 0.2886) * scale , y * scale), \
                   (((x * 0.866) + 0.866) * scale  , y * scale), \
                   (((x * 0.866) + 1.1547) * scale , (y + 0.5) * scale), \
                   (((x * 0.866) + 0.866) * scale  , (y + 1) * scale), \
                   (((x * 0.866) + 0.2886) * scale , (y + 1) * scale), \
                   ((x * 0.866) * scale          , (y + 0.5) * scale)
                ]

    @classmethod
    def neighbors(cls, x, y, br=BoundingRect()):
        if x % 2 == 0:
            return [(x, y - 1), (x + 1, y - 1), (x + 1, y), (x, y + 1), (x - 1, y), (x - 1, y - 1)]
        else:
            return [(x, y - 1), (x + 1, y), (x + 1, y + 1), (x, y + 1), (x - 1, y + 1), (x - 1, y)]

    @classmethod
    def line(cls, x1, y1, x2, y2, br=BoundingRect()):
        """ reimplemented from BaseGeometry.line
        Implementation of bresenham's algorithm """
        cls.assertCoordinates((x1, y1), (x2, y2))

        if (x1, y1) == (x2, y2):
            return [(x1, y1)]

        # vertical symmetry
        reversed_sym = (x1 > x2)
        if reversed_sym:
            x2, y2, x1, y1 = x1, y1, x2, y2


        # The unit that will be used is half the width of an hexagon: u = 0.5773
        # In that system, half-height of an hexagon is 0.8860u, or sqrt(3)/2 * u

        if abs(x2 - x1) < (2 * abs((y2 - y1)) + abs(x2 % 2) - abs(x1 % 1)):
            # vertical quadrants

            direction = 1 if y2 > y1 else -1

            dx = 1.5 * (x2 - x1)
            dy = direction * (y2 - y1)

            if (x1 + x2) % 2 == 1:
                if x1 % 2 == 0:
                    dy += direction * 0.5
                else:
                    dy -= direction * 0.5

            k = dx / (dy * sqrt(3))
            pas = sqrt(3) / 2

            result = []
            offset = 0.0
            pos = (x1, y1)
            result.append(pos)

            while pos != (x2, y2):
                offset += (k * pas)
                if offset <= 0.5:
                    x, y = pos
                    pos = x, y + direction
                    result.append(pos)
                    offset += (k * pas)
                else:
                    x, y = pos
                    if (x % 2 == 0 and direction == 1) or (x % 2 == 1 and direction == -1):
                        pos = x + 1, y
                    else:
                        pos = x + 1, y + direction
                    result.append(pos)
                    offset -= 1.5

                # in case of error in the algorithm, we should avoid infinite loop:
                if direction * pos[1] > direction * y2:
                    result = []
                    break

        else:
            # horizontal quadrants
            dx = x2 - x1
            dy = y2 - y1

            if (x1 + x2) % 2 == 1:
                dy += 0.5 if x1 % 2 == 0 else -0.5

            k = dy / dx
            pas = 1

            result = []
            d = 0.0
            pos = (x1, y1)
            result.append(pos)

            while pos != (x2, y2):
                d += k * pas
                if d > 0:
                    x, y = pos
                    if x % 2 == 0:
                        pos = x + 1, y
                    else:
                        pos = x + 1, y + 1
                    result.append(pos)
                    d -= 0.5
                else:
                    x, y = pos
                    if x % 2 == 0:
                        pos = x + 1, y - 1
                    else:
                        pos = x + 1, y
                    result.append(pos)
                    d += 0.5

                # in case of error in the algorithm, we should avoid infinite loop:
                if pos[0] > x2:
                    result = []
                    break

        if reversed_sym:
            result.reverse()
        return result

    @classmethod
    def triangle(cls, xa, ya, xh, yh, iAngle, br=BoundingRect()):
        """ reimplemented from BaseGeometry.triangle """
        cls.assertCoordinates((xa, ya), (xh, yh))
        cls._assertValidAngle(iAngle)

        if (xa, ya) == (xh, yh):
            return [(xa, ya)]

        result = []

        # convert to cubic coodinates (see 'cube_coords' lib)
        xua, yua, _ = cls.to_cubic(xa, ya)
        xuh, yuh, zuh = cls.to_cubic(xh, yh)

        # direction vector
        dx_dir, dy_dir = xuh - xua, yuh - yua

        # normal vector
        dx_n, dy_n = -(2 * dy_dir + dx_dir), (2 * dx_dir + dy_dir)
        dz_n = (-dx_n - dy_n)

        # B and C positions
        k = 1 / (iAngle * sqrt(3))
        xub, yub, zub = xuh + (k * dx_n), yuh + (k * dy_n), zuh + (k * dz_n)
        xuc, yuc, zuc = xuh + (-k * dx_n), yuh + (-k * dy_n), zuh + (-k * dz_n)

        xub, yub, zub = cls.cube_round(xub, yub, zub)
        xuc, yuc, zuc = cls.cube_round(xuc, yuc, zuc)

        xb, yb = cls.from_cubic(xub, yub, zub)
        xc, yc = cls.from_cubic(xuc, yuc, zuc)

        # sides
        segments = [(xa, ya, xb, yb), (xb, yb, xc, yc), (xc, yc, xa, ya)]

        # base (lower slope)
        x1, y1, x2, y2 = min(segments, key=lambda x: (abs ((x[3] - x[1]) / (x[2] - x[0])) if x[2] != x[0] else 10 ** 10))
        base = cls.line(x1, y1, x2, y2)
        y_base = y1
        segments.remove((x1, y1, x2, y2))

        # 'hat' (the 2 other sides)
        chapeau = []
        y_sommet = None
        for x1, y1, x2, y2 in segments:
            if y_sommet == None:
                y_sommet = y2
            chapeau.extend(cls.line(x1, y1, x2, y2))

        # sense (1 if top is under base, -1 if not)
        sens = 1 if y_sommet > y_base else -1

        # rove over y values from base to hat
        for x, y in base:
            while not (x, y) in chapeau:
                result.append((x, y))
                y += sens
        result.extend(chapeau)

        return result

    @classmethod
    def triangle3d(cls, xa, ya, za, xh, yh, zh, iAngle, br=BoundingRect()):
        """ reimplemented from BaseGeometry.triangle3d """
        cls.assertCoordinates((za, zh))
        flat_triangle = cls.triangle(xa, ya, xh, yh, iAngle)

        result = {}

        k = 1 / (iAngle * sqrt(3))

        # use cubic coordinates
        xua, yua, zua = cls.to_cubic(xa, ya)
        xuh, yuh, zuh = cls.to_cubic(xh, yh)

        length = max(abs(xuh - xua), abs(yuh - yua), abs(zuh - zua))

        vertical_line = SquareGeometry.line(0, za, length, zh)

        # build a dict with X key and value is a list of Z values
        vertical_line_dict = {d:[] for d, z in vertical_line}
        for d, z in vertical_line:
            vertical_line_dict[d].append(z)

        # this is approximative: height is update according to the manhattan distance to center
        for x, y in flat_triangle:
            xu, yu, zu = cls.to_cubic(x, y)
            distance = int(max(abs(xu - xua), abs(yu - yua), abs(zu - zua)))
            try:
                z_list = vertical_line_dict[ distance ]
            except KeyError:
                distance = length
                z_list = vertical_line_dict[ distance ]
            dh = int(k * distance) + 1 if distance > 0 else 0
            result[ (x, y) ] = ((min(z_list) - dh) , (max(z_list) + dh))
        return result

    @classmethod
    def rotate(cls, center, coordinates, rotations, br=BoundingRect()):
        """ reimplemented from BaseGeometry.rotate """
        cls.assertCoordinates(center, *coordinates)

        if coordinates == [center] or rotations % 6 == 0:
            return coordinates
        x0, y0 = center
        xu0, yu0, zu0 = cls.to_cubic(x0, y0)
        result = []

        for x, y in coordinates:
            xu, yu, zu = cls.to_cubic(x, y)
            dxu, dyu, dzu = xu - xu0, yu - yu0, zu - zu0
            for _ in range(rotations):
                dxu, dyu, dzu = -dzu, -dxu, -dyu
            xru, yru, zru = dxu + xu0, dyu + yu0, dzu + zu0
            xr, yr = cls.from_cubic(xru, yru, zru)
            result.append((xr, yr))
        return result
