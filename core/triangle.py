'''
Created on 8 nov. 2016
    Triangle algorithms
@author: olinox
'''

from math import sqrt

from core import bresenham, constants
from core.cube_coords import cv_off_cube, cube_round, cv_cube_off


ANGLES = [1, 2, 3]

def triangle(geometry, xa, ya, xh, yh, iAngle):
    if geometry == constants.SQUAREGRID:
        return triangle_sq(xa, ya, xh, yh, iAngle)
    elif geometry == constants.HEXGRID: 
        return triangle_hex(xa, ya, xh, yh, iAngle)
    else:
        raise ValueError("'geometry' has to be a value from GRID_GEOMETRIES")

def triangle3d(geometry, xa, ya, za, xh, yh, zh, iAngle):
    if geometry == constants.SQUAREGRID:
        return triangle_sq_3d(xa, ya, za, xh, yh, zh, iAngle)
    elif geometry == constants.HEXGRID: 
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
    base = bresenham.squ_2d_line(x1, y1, x2, y2)
    y_base = y1
    lines.remove( (x1, y1, x2, y2) )
    
    # 'hat' (2 other sides)
    hat = []
    y_top = None
    for x1, y1, x2, y2 in lines:
        if y_top == None: 
            y_top = y2
        hat.extend( bresenham.squ_2d_line(x1, y1, x2, y2) )
    
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

    vertical_line = bresenham.squ_2d_line(0, za, length, zh)
    
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
    base = bresenham.hex_2d_line(x1, y1, x2, y2)
    y_base = y1
    segments.remove( (x1, y1, x2, y2) )
    
    # 'hat' (the 2 other sides)
    chapeau = []
    y_sommet = None
    for x1, y1, x2, y2 in segments:
        if y_sommet == None: 
            y_sommet = y2
        chapeau.extend( bresenham.hex_2d_line(x1, y1, x2, y2) )
    
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
    
    if (xa, ya) == (xh, yh):
        return [(xa, ya)]   
    result = {} 
    
    k = 1 / ( iAngle * sqrt(3) )
    
    xua, yua, zua = cv_off_cube(xa, ya)
    xuh, yuh, zuh = cv_off_cube(xh, yh)
    
    length = max( abs(xuh - xua), abs(yuh - yua), abs(zuh - zua) )

    vertical_line = bresenham.squ_2d_line(0, za, length, zh)
    
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

    
