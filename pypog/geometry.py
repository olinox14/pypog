'''
    Geometric functions on hexagonal or square grids

    2D functions return lists of (x, y) coordinates
    3D functions return lists of (x, y, z) coordinates

    * neighbours_of function return the list of the cells around the (x, y) cell
    * zone function return the list of the cells surrounding the (x, y) cell within a 'radius' distance
    * line2d function return the list of the cells on a line between the (x1, y1) cell and the (x2, y2) cell
    * line3d function return the list of the cells on a line between the (x1, y1, z1) cell and the (x2, y2, z2) cell
    * rect function return the list of the cells in the rectangle between the cells (x1, y1), (x2, y1), , (x2, y2) and , (x1, y2)
    * hollow_rect function return the list of the cells on the borders of the rectangle between the cells (x1, y1), (x2, y1), , (x2, y2) and , (x1, y2)
    * triangle function return the list of the cells in a triangle from its apex (xa, ya) to its base (xh, yh)
    * triangle3d function return the list of the cells in a cone from its apex (xa, ya, za) to its base (xh, yh, zh)
    * pivot function return a list of coordinates after a counterclockwise rotation of a given list of coordinates, around a given center


    ** By Cro-Ki l@b, 2017 **
'''
from math import sqrt

CELL_SHAPES = (4, 6)

SQUARE = 4
FLAT_HEX = 61
TOP_HEX = 62
CELL_SHAPES = (SQUARE, FLAT_HEX, TOP_HEX)

ANGLES = (1, 2, 3)

class UnknownCellShape(ValueError): pass



# ## NEIGHBOURS

def neighbours(cell_shape, x, y):
    """ returns the list of coords of the neighbours of a cell"""
    if cell_shape == SQUARE:
        return squ_neighbours(x, y)
    elif cell_shape == FLAT_HEX:
        return fhex_neighbours(x, y)
    else:
        raise ValueError("'cell_shape' has to be a value from CELL_SHAPES")

def fhex_neighbours(x, y):
    """ returns the list of coords of the neighbours of a cell on an hexagonal grid"""
    if x % 2 == 0:
        return [(x, y - 1), (x + 1, y - 1), (x + 1, y), (x, y + 1), (x - 1, y), (x - 1, y - 1)]
    else:
        return [(x, y - 1), (x + 1, y), (x + 1, y + 1), (x, y + 1), (x - 1, y + 1), (x - 1, y)]

def squ_neighbours(x, y):
    """ returns the list of coords of the neighbours of a cell on an square grid"""
    return [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1), \
            (x - 1, y), (x + 1, y)  , \
            (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)]

def zone(cell_shape, x0, y0, radius):
    """ returns the list of the coordinates of the cells in the zone around (x0, y0)
    """
    if not all(isinstance(c, int) for c in [x0, y0, radius]):
        raise TypeError("x0, y0, radius have to be integers")
    if not radius >= 0:
        raise ValueError("radius has to be positive")
    buffer = frozenset([ (x0, y0) ])

    for _ in range(0, radius):
        current = buffer
        for x, y in current:
            buffer |= frozenset(neighbours(cell_shape, x, y))

    return list(buffer)


# ## LINES (implementations of bresenham algorithm)

def line2d(cell_shape, x1, y1, x2, y2):
    """returns a line from x1,y1 to x2,y2
    grid could be one of the GRIDTYPES values"""
    if not all(isinstance(c, int) for c in [x1, y1, x2, y2]):
        raise TypeError("x1, y1, x2, y2 have to be integers")
    if cell_shape == FLAT_HEX:
        return fhex_line(x1, y1, x2, y2)
    elif cell_shape == SQUARE:
        return squ2_line(x1, y1, x2, y2)
    else:
        raise ValueError("'cell_shape' has to be a value from CELL_SHAPES")

def line3d(cell_shape, x1, y1, z1, x2, y2, z2):
    """returns a line from x1,y1,z1 to x2,y2,z2
    grid could be one of the GRIDTYPES values"""
    if not all(isinstance(c, int) for c in [z1, z2]):
        raise TypeError("x1, y1, z1, x2, y2, z2 have to be integers")
    hoLine = line2d(cell_shape, x1, y1, x2, y2)
    if z1 == z2:
        return [(x, y, z1) for x, y in hoLine]
    else:
        ligneZ = squ2_line(0, z1, (len(hoLine) - 1), z2)
        return [(hoLine[d][0], hoLine[d][1], z) for d, z in ligneZ]

def squ2_line(x1, y1, x2, y2):
    """Line Bresenham algorithm for square grid"""
    result = []

    if (x1, y1) == (x2, y2):
        return [(x1, y1)]

    # DIAGONAL SYMETRY
    V = (abs(y2 - y1) > abs(x2 - x1))
    if V: y1, x1, y2, x2 = x1, y1, x2, y2

    # VERTICAL SYMETRY
    reversed_sym = (x1 > x2)
    if reversed_sym:
        x2, y2, x1, y1 = x1, y1, x2, y2

    DX = x2 - x1 ; DY = y2 - y1
    offset = 0.0
    step = 1 if DY > 0 else -1
    alpha = (abs(DY) / DX)

    y = y1
    for x in range(x1, x2 + 1):
        coord = (y, x) if V else (x, y)
        result.append(coord)

        offset += alpha
        if offset > 0.5:
            y += step
            offset -= 1.0

    if reversed_sym:
        result.reverse()
    return result

def fhex_line(x1, y1, x2, y2):
    """Line Bresenham algorithm for hexagonal grid"""
    if (x1, y1) == (x2, y2):
        return [(x1, y1)]

    reversed_sym = (x1 > x2)
    if reversed_sym:
        x1, x2 = x2, x1
        y1, y2 = y2, y1

    if abs(x2 - x1) < (2 * abs((y2 - y1)) + abs(x2 % 2) - abs(x1 % 1)):
        # vertical quadrants

        # unit is half the width: u = 0.5773
        # half-height is then 0.8860u, or sqrt(3)/2
        direction = 1 if y2 > y1 else -1

        dx = 1.5 * (x2 - x1)
        dy = direction * (y2 - y1)
        if (x1 + x2) % 2 == 1:
            if x1 % 2 == 0:
                dy += direction * 0.5
            else:
                dy -= direction * 0.5

        k = dx / (dy * sqrt(3))
        pas = 0.5 * sqrt(3)

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
        dx = x2 - x1 ; dy = y2 - y1
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


# ## RECTANGLES

def rectangle(x1, y1, x2, y2):
    """return a list of cells in a rectangle between (X1, Y1), (X2, Y2)"""
    if not all(isinstance(val, int) for val in [x1, y1, x2, y2]):
        raise TypeError("x1, y1, x2, y2 should be integers")
    xa, ya, xb, yb = min([x1, x2]), min([y1, y2]), max([x1, x2]), max([y1, y2])
    return [(x, y) for x in range(xa, xb + 1) for y in range(ya, yb + 1)]

def hollow_rectangle(x1, y1, x2, y2):
    """return a list of cells composing the sides of the rectangle between (X1, Y1), (X2, Y2)"""
    if not all(isinstance(val, int) for val in [x1, y1, x2, y2]):
        raise TypeError("x1, y1, x2, y2 should be integers")
    return [(x, y) for x, y in rectangle(x1, y1, x2, y2)
            if (x == x1 or x == x2 or y == y1 or y == y2)]


# ## TRIANGLES

def triangle(cell_shape, xa, ya, xh, yh, iAngle):
    """Returns a list of (x, y) coordinates in a triangle
    A is the top of the triangle, H if the middle of the base
    """
    if not all(isinstance(c, int) for c in [xa, ya, xh, yh]):
        raise TypeError("xa, ya, xh, yh should be integers")
    if not iAngle in ANGLES:
        raise ValueError("iAngle should be one of the ANGLES values")

    if cell_shape == SQUARE:
        return squ2_triangle(xa, ya, xh, yh, iAngle)
    elif cell_shape == FLAT_HEX:
        return fhex2_triangle(xa, ya, xh, yh, iAngle)
    else:
        raise ValueError("'cell_shape' has to be a value from CELL_SHAPES")

def triangle3d(cell_shape, xa, ya, za, xh, yh, zh, iAngle):
    """Returns a list of (x, y, z) coordinates in a 3d-cone
    A is the top of the cone, H if the center of the base

    WARNING: result is a dictionnary of the form {(x, y): (-z, +z)}

    This is for performance reason, because on a 2d grid, you generrally don't need a complete list of z coordinates
    as you don't want to display them: you just want to know if an altitude is inside a range.

    That could change in later version
    """
    # TODO: review the result form

    if not all(isinstance(c, int) for c in [za, zh]):
        raise TypeError("xa, ya, za, xh, yh, zh should be integers")
        # a triangle2d will be built during algo, so other args will be checked later

    if cell_shape == SQUARE:
        return squ3_triangle(xa, ya, za, xh, yh, zh, iAngle)
    elif cell_shape == FLAT_HEX:
        return fhex3_triangle(xa, ya, za, xh, yh, zh, iAngle)
    else:
        raise ValueError("'cell_shape' has to be a value from CELL_SHAPES")


def squ2_triangle(xa, ya, xh, yh, iAngle):
    """ triangle algorithm on square grid
    """
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
    base = line2d(SQUARE, x1, y1, x2, y2)
    y_base = y1
    lines.remove((x1, y1, x2, y2))

    # 'hat' (2 other sides)
    hat = []
    y_top = None
    for x1, y1, x2, y2 in lines:
        if y_top == None:
            y_top = y2
        hat.extend(line2d(SQUARE, x1, y1, x2, y2))

    # sense (1 if top is under base, -1 if not)
    sense = 1 if y_top > y_base else -1

    # rove over y values from base to hat
    for x, y in base:
        while not (x, y) in hat:
            result.append((x, y))
            y += sense
    result.extend(hat)

    return result

def fhex2_triangle(xa, ya, xh, yh, iAngle):
    """  triangle algorithm on hexagonal grid
    """
    if (xa, ya) == (xh, yh):
        return [(xa, ya)]

    result = []

    # convert to cubic coodinates (see 'cube_coords' lib)
    xua, yua, _ = cv_off_cube(xa, ya)
    xuh, yuh, zuh = cv_off_cube(xh, yh)

    # direction vector
    dx_dir, dy_dir = xuh - xua, yuh - yua

    # normal vector
    dx_n, dy_n = -(2 * dy_dir + dx_dir), (2 * dx_dir + dy_dir)
    dz_n = (-dx_n - dy_n)

    # B and C positions
    k = 1 / (iAngle * sqrt(3))
    xub, yub, zub = xuh + (k * dx_n), yuh + (k * dy_n), zuh + (k * dz_n)
    xuc, yuc, zuc = xuh + (-k * dx_n), yuh + (-k * dy_n), zuh + (-k * dz_n)

    xub, yub, zub = cube_round(xub, yub, zub)
    xuc, yuc, zuc = cube_round(xuc, yuc, zuc)

    xb, yb = cv_cube_off(xub, yub, zub)
    xc, yc = cv_cube_off(xuc, yuc, zuc)

    # sides
    segments = [(xa, ya, xb, yb), (xb, yb, xc, yc), (xc, yc, xa, ya)]

    # base (lower slope)
    x1, y1, x2, y2 = min(segments, key=lambda x: (abs ((x[3] - x[1]) / (x[2] - x[0])) if x[2] != x[0] else 10 ** 10))
    base = line2d(FLAT_HEX, x1, y1, x2, y2)
    y_base = y1
    segments.remove((x1, y1, x2, y2))

    # 'hat' (the 2 other sides)
    chapeau = []
    y_sommet = None
    for x1, y1, x2, y2 in segments:
        if y_sommet == None:
            y_sommet = y2
        chapeau.extend(line2d(FLAT_HEX, x1, y1, x2, y2))

    # sense (1 if top is under base, -1 if not)
    sens = 1 if y_sommet > y_base else -1

    # rove over y values from base to hat
    for x, y in base:
        while not (x, y) in chapeau:
            result.append((x, y))
            y += sens
    result.extend(chapeau)

    return result


def squ3_triangle(xa, ya, za, xh, yh, zh, iAngle):
    """ 3d triangle algorithm on square grid"""
    result = []

    flat_triangle = triangle(SQUARE, xa, ya, xh, yh, iAngle)
    k = 1 / (iAngle * sqrt(3))

    length = max(abs(xh - xa), abs(yh - ya))

    vertical_line = line2d(SQUARE, 0, za, length, zh)

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

def fhex3_triangle(xa, ya, za, xh, yh, zh, iAngle):
    """ 3d triangle algorithm on hexagonal grid """

    flat_triangle = triangle(FLAT_HEX, xa, ya, xh, yh, iAngle)

    result = {}

    k = 1 / (iAngle * sqrt(3))

    # use cubic coordinates
    xua, yua, zua = cv_off_cube(xa, ya)
    xuh, yuh, zuh = cv_off_cube(xh, yh)

    length = max(abs(xuh - xua), abs(yuh - yua), abs(zuh - zua))

    vertical_line = line2d(SQUARE, 0, za, length, zh)

    # build a dict with X key and value is a list of Z values
    vertical_line_dict = {d:[] for d, z in vertical_line}
    for d, z in vertical_line:
        vertical_line_dict[d].append(z)

    # this is approximative: height is update according to the manhattan distance to center
    for x, y in flat_triangle:
        xu, yu, zu = cv_off_cube(x, y)
        distance = int(max(abs(xu - xua), abs(yu - yua), abs(zu - zua)))
        try:
            z_list = vertical_line_dict[ distance ]
        except KeyError:
            distance = length
            z_list = vertical_line_dict[ distance ]
        dh = int(k * distance) + 1 if distance > 0 else 0
        result[ (x, y) ] = ((min(z_list) - dh) , (max(z_list) + dh))
    return result


# ## TRANSLATIONS / ROTATIONS

def pivot(cell_shape, center, coordinates, rotations):
    """pivot 'rotations' times the coordinates (list of (x, y) tuples)
    around the center coordinates (x,y)
    Rotation is counterclockwise"""
    # check the args:
    try:
        x, y = center
    except ValueError:
        raise TypeError("'center' should be an tuple of (x, y) coordinates with x and y integers (given: {})".format(center))
    if not isinstance(x, int) or not isinstance(y, int):
        raise ValueError("'center' should be an tuple of (x, y) coordinates with x and y integers (given: {})".format(center))

    try:
        for coord in coordinates:
            try:
                x, y = coord
                if not isinstance(x, int) or not isinstance(y, int):
                    raise ValueError()
            except ValueError:
                raise ValueError("'coordinates' should be an list of (x, y) coordinates with x and y integers (given: {})".format(coordinates))
    except TypeError:
        raise TypeError("'coordinates' should be an list of (x, y) coordinates with x and y integers (given: {})".format(coordinates))

    if not isinstance(rotations, int):
        raise TypeError("'rotations' should be an integer (given: {})".format(rotations))

    # call the method according to cells shape
    if cell_shape == SQUARE:
        return squ_pivot(center, coordinates, rotations)
    elif cell_shape == FLAT_HEX:
        return fhex_pivot(center, coordinates, rotations)
    else:
        raise ValueError("'cell_shape' has to be a value from CELL_SHAPES")


def fhex_pivot(center, coordinates, rotations):
    """pivot 'rotations' times the coordinates (list of (x, y) tuples)
    around the center coordinates (x,y)
    On hexagonal grid, rotates of 60 degrees each time"""
    if coordinates == [center] or rotations % 6 == 0:
        return coordinates
    x0, y0 = center
    xu0, yu0, zu0 = cv_off_cube(x0, y0)
    result = []

    for x, y in coordinates:
        xu, yu, zu = cv_off_cube(x, y)
        dxu, dyu, dzu = xu - xu0, yu - yu0, zu - zu0
        for _ in range(rotations):
            dxu, dyu, dzu = -dzu, -dxu, -dyu
        xru, yru, zru = dxu + xu0, dyu + yu0, dzu + zu0
        xr, yr = cv_cube_off(xru, yru, zru)
        result.append((xr, yr))
    return result

def squ_pivot(center, coordinates, rotations):
    """pivot 'rotations' times the coordinates (list of (x, y) tuples)
    around the center coordinates (x,y)
    On square grid, rotates of 90 degrees each time"""
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


# ## CUBIC COORDINATES
def cv_cube_off(xu, yu, zu):
    """convert cubic coordinates (xu, yu, zu) in standards coordinates (x, y) [offset]"""
    y = int(xu + (zu - (zu & 1)) / 2)
    x = zu
    return (x, y)

def cv_off_cube(x, y):
    """converts standards coordinates (x, y) [offset] in cubic coordinates (xu, yu, zu)"""
    zu = x
    xu = int(y - (x - (x & 1)) / 2)
    yu = int(-xu - zu)
    return (xu, yu, zu)

# > unused
def cube_round(x, y, z):
    """returns the nearest cell (in cubic coords)
    x, y, z can be floating numbers, no problem."""
    rx, ry, rz = round(x), round(y), round(z)
    x_diff, y_diff, z_diff = abs(rx - x), abs(ry - y), abs(rz - z)
    if x_diff > y_diff and x_diff > z_diff:
        rx = -ry - rz
    elif y_diff > z_diff:
        ry = -rx - rz
    else:
        rz = -rx - ry
    return (rx, ry, rz)

# > unused
def hex_distance_cube(xa, ya, za, xb, yb, zb):
    """returns the manhattan distance between the two cells"""
    return max(abs(xa - xb), abs(ya - yb), abs(za - zb))

# > unused
def distance_off(xa, ya, xb, yb):
    """ distance between A and B (offset coordinates)"""
    # 10 times quicker if no conversion...
    xua, yua, zua = cv_off_cube(xa, ya)
    xub, yub, zub = cv_off_cube(xb, yb)
    return max(abs(xua - xub), abs(yua - yub), abs(zua - zub))
