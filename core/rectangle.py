'''
Created on 8 nov. 2016
    Rectangle algorythms
    rectangles are assumed to be composed of vertical/horizontal sides
@author: olinox
'''

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
    
    