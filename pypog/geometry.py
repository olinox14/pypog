'''
Created on 5 dec. 2016
    Geometric functions on hexagonal or square grids
    
    > Line algorithm is an implementation of bresenham algorithm
    
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
    
@author: olinox
'''
from math import sqrt


GRID_GEOMETRIES = (4, 5)
SQUARE = 4
HEX = 5
ANGLES = (1, 2, 3)

## neigbours

def neighbours_of(cell_shape, x, y):
    if cell_shape == SQUARE:
        return squ_neighbours_of(x, y)
    elif cell_shape == HEX: 
        return hex_neighbours_of(x, y)
    else:
        raise ValueError("'geometry' has to be a value from GRID_GEOMETRIES")

def hex_neighbours_of(x, y):
    """ returns the list of coords of the neighbours of a cell on an hexagonal grid"""
    if x%2 == 0:
        return [(x, y-1), (x+1, y-1), (x+1, y), (x,  y+1), (x-1, y), (x-1, y-1)]
    else:
        return [(x, y-1), (x+1, y), (x+1, y+1), (x,  y+1), (x-1, y+1), (x-1, y)]        

def squ_neighbours_of(x, y):
    """ returns the list of coords of the neighbours of a cell on an square grid"""
    return [(x-1, y-1), (x, y-1), (x+1, y-1), \
            (x-1, y), (x+1, y)  , \
            (x-1, y+1), (x, y+1),(x+1, y+1)]
    


## zones

def zone(cell_shape, x0, y0, radius):
    """ returns the list of the coordinates of the cells in the zone around (x0, y0)
    """
    if not all(isinstance(c, int) for c in [x0, y0, radius]):
        raise TypeError("x0, y0, radius have to be integers")
    if not radius >= 0:
        raise ValueError("radius has to be positive")
    buffer = frozenset( [ (x0, y0) ] )

    for _ in range(0, radius):
        current = buffer
        for x, y in current:
            buffer |= frozenset( neighbours_of( cell_shape, x, y ) )

    return list(buffer)


## line : bresenham algorithm

def line2d(cell_shape, x1, y1, x2, y2):
    """returns a line from x1,y1 to x2,y2
    grid could be one of the GRIDTYPES values"""
    if not all(isinstance(c, int) for c in [x1, y1, x2, y2]):
        raise TypeError("x1, y1, x2, y2 have to be integers")
    if (x1, y1) == (x2, y2):
        return [(x1, y1)]
    if cell_shape == HEX:
        return hex_2d_line(x1, y1, x2, y2)
    elif cell_shape == SQUARE: 
        return squ_2d_line(x1, y1, x2, y2)
    else:
        raise ValueError("'geometry' has to be a value from GRID_GEOMETRIES")

def line3d(cell_shape, x1, y1, z1, x2, y2, z2):
    """returns a line from x1,y1,z1 to x2,y2,z2
    grid could be one of the GRIDTYPES values"""
    if not all(isinstance(c, int) for c in [x1, y1, z1, x2, y2, z2]):
        raise TypeError("x1, y1, z1, x2, y2, z2 have to be integers")
    hoLine = line2d(cell_shape, x1, y1, x2, y2)
    if z1 == z2:
        return [(x, y, z1) for x, y in hoLine]
    else:
        ligneZ = _brC(0, z1, (len(hoLine)-1), z2)
        return [(hoLine[d][0], hoLine[d][1], z) for d, z in ligneZ]

def hex_2d_line(x1, y1, x2, y2):
    """returns a line from x1,y1 to x2,y2 on an hexagonal grid
    line is a list of coordinates"""
    if (x1, y1) == (x2, y2):
        return [(x1, y1)]
    return _brH(x1, y1, x2, y2)

def hex_3d_line(x1, y1, z1, x2, y2, z2):
    """returns a line from x1,y1,z1 to x2,y2,z2 on an hexagonal grid
    line is a list of coordinates"""
    hoLine = hex_2d_line(x1, y1, x2, y2)
    if z1 == z2:
        return [(x, y, z1) for x, y in hoLine]
    else:
        zLine = _brC(0, z1, (len(hoLine)-1), z2)
        dicZ = {d:[] for d, z in zLine}
        for d, z in zLine:
            dicZ[d].append(z)
        return [(hoLine[d][0], hoLine[d][1], z) for d, liste_z in dicZ.items() for z in liste_z]

def squ_2d_line(x1, y1, x2, y2):
    """returns a line from x1,y1 to x2,y2 on an square grid
    line is a list of coordinates
    """
    if (x1, y1) == (x2, y2):
        return [(x1, y1)]
    return _brC(x1, y1, x2, y2)
    
def squ_3d_line(x1, y1, z1, x2, y2, z2):
    """returns a line from x1,y1,z1 to x2,y2,z2 on an square grid
    line is a list of coordinates"""
    hoLine = squ_2d_line(x1, y1, x2, y2)
    if z1 == z2:
        return [(x, y, z1) for x, y in hoLine]
    else:
        zLine = _brC(0, z1, (len(hoLine)-1), z2)
        return [(hoLine[d][0], hoLine[d][1], z) for d, z in zLine]

def _brC(x1, y1, x2, y2):
    """Line Bresenham algorithm for square grid"""
    result = []
    
    # DIAGONAL SYMETRY
    V = ( abs(y2 - y1) > abs(x2 - x1) )
    if V: y1, x1, y2, x2 = x1, y1, x2, y2
    
    # VERTICAL SYMETRY
    reversed_sym = (x1 > x2)
    if reversed_sym:  
        x2, y2, x1, y1 = x1, y1, x2, y2
    
    DX = x2 - x1 ; DY = y2 - y1
    offset = 0.0
    step = 1 if DY > 0 else -1
    alpha = ( abs( DY ) / DX )
    
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
    
def _brH(x1, y1, x2, y2):
    """Line Bresenham algorithm for hexagonal grid"""
    reversed_sym = (x1 > x2)
    if reversed_sym:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
    
    if abs(x2 - x1) < (2*abs((y2-y1)) + abs(x2 % 2) - abs(x1 % 1)):
        result = _brH_v(x1, y1, x2, y2)
    else:
        result = _brH_h(x1, y1, x2, y2)   

    if reversed_sym: 
        result.reverse()
    return result
         
def _brH_h(x1, y1, x2, y2):
    """Line Bresenham algorithm for hexagonal grid (horizontal quadrants)"""  
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
        d += k*pas
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
        
        if pos[0] > x2:
            result = []
            break
                      
    return result
     
def _brH_v(x1, y1, x2, y2):
    """Line Bresenham algorithm for hexagonal grid (vertical quadrants)"""  
    # unit is half the width: u = 0.5773
    # half-height is then 0.8860u, or sqrt(3)/2
    direction = 1 if y2 > y1 else -1
 
    dx = 1.5 * (x2 - x1)  
    dy = direction * (y2 - y1)    
    if (x1 + x2) % 2 == 1: 
        if x1 % 2 == 0:
            dy += direction*0.5
        else:
            dy -= direction*0.5
 
    k = dx/(dy*sqrt(3)) 
    pas = 0.5*sqrt(3)
 
    result = []
    offset = 0.0
    pos = (x1, y1)
    result.append(pos)
    
    while pos != (x2, y2):
        offset += (k*pas)
        if offset <= 0.5:
            x, y = pos
            pos = x, y + direction
            result.append(pos)
            offset += (k*pas)
        else:
            x, y = pos
            if (x %2 == 0 and direction == 1) or (x % 2 == 1 and direction == -1):
                pos = x + 1, y
            else:
                pos = x + 1, y + direction            
            result.append(pos)
            offset -= 1.5
        
        if direction*pos[1] > direction*y2:
            result = []
            break
 
    return result 


## rectangles

def rect(x1, y1, x2, y2):
    """return a list of cells in a rectangle between (X1, Y1), (X2, Y2)"""
    if not all(isinstance(val, int) for val in [x1, y1, x2, y2]):
        raise TypeError("x1, y1, x2, y2 should be integers")
    xa, ya, xb, yb = min([x1, x2]), min([y1, y2]), max([x1, x2]), max([y1, y2])
    return [(x, y) for x in range(xa, xb + 1) for y in range(ya, yb + 1)]

def hollow_rect(x1, y1, x2, y2):
    """return a list of cells composing the sides of the rectangle between (X1, Y1), (X2, Y2)"""
    if not all(isinstance(val, int) for val in [x1, y1, x2, y2]):
        raise TypeError("x1, y1, x2, y2 should be integers")
    return [(x, y) for x, y in rect(x1, y1, x2, y2)
            if (x == x1 or x == x2 or y == y1 or y == y2)]
    
    
    
## triangles
    


def triangle(cell_shape, xa, ya, xh, yh, iAngle):
    if cell_shape == SQUARE:
        return triangle_sq(xa, ya, xh, yh, iAngle)
    elif cell_shape == HEX: 
        return triangle_hex(xa, ya, xh, yh, iAngle)
    else:
        raise ValueError("'geometry' has to be a value from GRID_GEOMETRIES")

def triangle3d(cell_shape, xa, ya, za, xh, yh, zh, iAngle):
    if cell_shape == SQUARE:
        return triangle_sq_3d(xa, ya, za, xh, yh, zh, iAngle)
    elif cell_shape == HEX: 
        return triangle_hex_3d(xa, ya, za, xh, yh, zh, iAngle)
    else:
        raise ValueError("'geometry' has to be a value from GRID_GEOMETRIES")

def triangle_sq(xa, ya, xh, yh, iAngle):   
    """Returns a list of (x, y) coordinates in a triangle
    A is the top of the triangle, H if the middle of the base
    (square grid)
    """
    if not all(isinstance(c, int) for c in [xa, ya, xh, yh]):
        raise TypeError("xa, ya, xh, yh should be integers")
    if not iAngle in ANGLES:
        raise ValueError("iAngle should be one of the ANGLES values")
    if (xa, ya) == (xh, yh):
        return [(xa, ya)]    
    
    result = []
    
    # direction vector
    dx_dir, dy_dir = xh - xa, yh - ya
    
    # normal vector
    dx_n, dy_n = - dy_dir, dx_dir

    # B and C positions
    k = 1 / ( iAngle * sqrt(3) )
    xb, yb = xh + (k * dx_n), yh + (k * dy_n)
    xc, yc = xh + (-k * dx_n), yh + (-k * dy_n)
    
    xb, yb = round(xb), round(yb)
    xc, yc = round(xc), round(yc)

    # sides:
    lines = [(xa, ya, xb, yb), (xb, yb, xc, yc), (xc, yc, xa, ya)]
    
    # base (lower slope)
    x1, y1, x2, y2 = min(lines, key=lambda x: (abs ( (x[3] - x[1]) / (x[2] - x[0]) ) if x[2] != x[0] else 10**10))
    base = squ_2d_line(x1, y1, x2, y2)
    y_base = y1
    lines.remove( (x1, y1, x2, y2) )
    
    # 'hat' (2 other sides)
    hat = []
    y_top = None
    for x1, y1, x2, y2 in lines:
        if y_top == None: 
            y_top = y2
        hat.extend( squ_2d_line(x1, y1, x2, y2) )
    
    # sense (1 if top is under base, -1 if not)
    sense = 1 if y_top > y_base else -1
    
    # rove over y values from base to hat
    for x, y in base:
        while not (x, y) in hat:
            result.append( (x, y) )
            y += sense
    result.extend(hat)

    return result

def triangle_sq_3d(xa, ya, za, xh, yh, zh, iAngle):
    """returns a dictionnary {coord: (-dh, +dh)}
    coord keys are the cells in the triangle, (-dh, +dh) value is the vertical amplitude"""
    
    #TODO: review result form
    
    if not all(isinstance(c, int) for c in [xa, ya, xh, yh]):
        raise TypeError("xa, ya, za, xh, yh have to be integers")
    if not iAngle in ANGLES:
        raise ValueError("iAngle should be one of the ANGLES values")
    if (xa, ya) == (xh, yh):
        return [(xa, ya)]  

    result = {} 
    
    flat_triangle = triangle_sq(xa, ya, xh, yh, iAngle)
    k = 1 / ( iAngle * sqrt(3) )

    length = max( abs(xh - xa), abs(yh - ya) )

    vertical_line = squ_2d_line(0, za, length, zh)
    
    #on cree un dictionnaire ou x est la cle, et ou la valeur est une liste de z
    vertical_line_dict = {d:[] for d, z in vertical_line}
    for d, z in vertical_line:
        vertical_line_dict[d].append(z)
        
    #approximation: on met a jour la hauteur en fonction de la distance au centre
    for x, y in flat_triangle:
        distance = int( max( abs(x - xa), abs(y - ya) ) )
        try:
            z_list = vertical_line_dict[ distance ]
        except KeyError:
            distance = length
            z_list = vertical_line_dict[ distance ]
        dh = int( k * distance ) + 1 if distance > 0 else 0
        result[ (x, y) ] = ( (min(z_list) - dh) , (max(z_list) + dh) ) 
    return result


def triangle_hex(xa, ya, xh, yh, iAngle):   
    """Returns a list of (x, y) coordinates in a triangle
    A is the top of the triangle, H if the middle of the base
    (hexagonal grid)
    """
    if not all(isinstance(c, int) for c in [xa, ya, xh, yh]):
        raise TypeError("xa, ya, xh, yh should be integers")
    if not iAngle in [1, 2, 3]:
        raise ValueError("iAngle should be one of the ANGLES values")
    if (xa, ya) == (xh, yh):
        return [(xa, ya)]    
    
    result = []
    
    # convert to cubic coodinates (see 'cube_coords' lib)
    xua, yua, _ = cv_off_cube( xa, ya )
    xuh, yuh, zuh = cv_off_cube( xh, yh )
    
    # direction vector
    dx_dir, dy_dir = xuh - xua, yuh - yua
    
    # normal vector
    dx_n, dy_n = - (2* dy_dir + dx_dir ), (2* dx_dir + dy_dir ) 
    dz_n = (- dx_n - dy_n)        

    # B and C positions
    k = 1 / ( iAngle * sqrt(3) )
    xub, yub, zub = xuh + (k * dx_n), yuh + (k * dy_n), zuh + (k * dz_n)
    xuc, yuc, zuc = xuh + (-k * dx_n), yuh + (-k * dy_n), zuh + (-k * dz_n)
    
    xub, yub, zub = cube_round(xub, yub, zub)
    xuc, yuc, zuc = cube_round(xuc, yuc, zuc)
    
    xb, yb = cv_cube_off(xub, yub, zub)
    xc, yc = cv_cube_off(xuc, yuc, zuc)

    # sides
    segments = [(xa, ya, xb, yb), (xb, yb, xc, yc), (xc, yc, xa, ya)]
    
    # base (lower slope)
    x1, y1, x2, y2 = min(segments, key=lambda x: (abs ( (x[3] - x[1]) / (x[2] - x[0]) ) if x[2] != x[0] else 10**10))
    base = hex_2d_line(x1, y1, x2, y2)
    y_base = y1
    segments.remove( (x1, y1, x2, y2) )
    
    # 'hat' (the 2 other sides)
    chapeau = []
    y_sommet = None
    for x1, y1, x2, y2 in segments:
        if y_sommet == None: 
            y_sommet = y2
        chapeau.extend( hex_2d_line(x1, y1, x2, y2) )
    
    # sense (1 if top is under base, -1 if not)
    sens = 1 if y_sommet > y_base else -1
    
    # rove over y values from base to hat
    for x, y in base:
        while not (x, y) in chapeau:
            result.append( (x, y) )
            y += sens
    result.extend(chapeau)

    return result

def triangle_hex_3d(xa, ya, za, xh, yh, zh, iAngle):
    """returns a dictionnary {coord: (-dh, +dh)}
    coord (x,y) keys are the cells in the triangle, 
    (-dh, +dh) value is the vertical amplitude"""
    flat_trangle = triangle_hex(xa, ya, xh, yh, iAngle)
    
    #TODO: review result form
    
    if (xa, ya) == (xh, yh):
        return [(xa, ya)]   
    result = {} 
    
    k = 1 / ( iAngle * sqrt(3) )
    
    xua, yua, zua = cv_off_cube(xa, ya)
    xuh, yuh, zuh = cv_off_cube(xh, yh)
    
    length = max( abs(xuh - xua), abs(yuh - yua), abs(zuh - zua) )

    vertical_line = squ_2d_line(0, za, length, zh)
    
    #on cree un dictionnaire ou x est la cle, et ou la valeur est une liste de z
    vertical_line_dict = {d:[] for d, z in vertical_line}
    for d, z in vertical_line:
        vertical_line_dict[d].append(z)
        
    #approximation: on met a jour la hauteur en fonction de la distance au centre
    for x, y in flat_trangle:
        xu, yu, zu = cv_off_cube(x, y)
        distance = int( max( abs(xu - xua), abs(yu - yua), abs(zu - zua) ) )
        try:
            z_list = vertical_line_dict[ distance ]
        except KeyError:
            distance = length
            z_list = vertical_line_dict[ distance ]
        dh = int( k * distance ) + 1 if distance > 0 else 0
        result[ (x, y) ] = ( (min(z_list) - dh) , (max(z_list) + dh) ) 
    return result


## cubic coordinates
def cv_cube_off(xu, yu, zu):
    """convert cubic coordinates (xu, yu, zu) in standards coordinates (x, y) [offset]"""
    if not all(isinstance(c, int) for c in [xu, yu, zu]):
        raise TypeError("!err: xu, yu et zu doivent etre des entiers")
    y = int( xu + ( zu - (zu & 1) ) / 2 )
    x = zu
    return (x, y)        

def cv_off_cube(x, y):
    """converts standards coordinates (x, y) [offset] in cubic coordinates (xu, yu, zu)"""
    if not all(isinstance(c, int) for c in [x, y]):
        raise TypeError("!err: x et y doivent etre des entiers")
    zu = x
    xu = int( y - ( x - (x & 1) ) / 2 )
    yu = int( -xu -zu )
    return (xu, yu, zu)    

def cube_round(x, y, z):
    """returns the nearest cell (in cubic coords)
    x, y, z can be floating numbers, no problem."""
    rx, ry, rz = round(x), round(y), round(z)
    x_diff, y_diff, z_diff = abs(rx - x), abs(ry - y), abs(rz - z)
    if x_diff > y_diff and x_diff > z_diff:
        rx = -ry-rz
    elif y_diff > z_diff:
        ry = -rx-rz
    else:
        rz = -rx-ry
    return (rx, ry, rz)

def hex_distance_cube(xa, ya, za, xb, yb, zb):
    """returns the manhattan distance between the two cells"""
    return max(abs(xa - xb), abs(ya - yb), abs(za - zb))

def distance_off(xa, ya, xb, yb):
        """ distance between A and B (offset coordinates)"""
        # 10 times quicker if no conversion...
        xua, yua, zua = cv_off_cube(xa, ya)
        xub, yub, zub = cv_off_cube(xb, yb)
        return max(abs(xua - xub), abs(yua - yub), abs(zua - zub))
    


    
    
    