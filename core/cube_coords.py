'''
Created on 8 nov. 2016
    Cubic coordinates are used in some algorythms about hexagonal grids
@author: olinox
'''


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
    
