'''
Created on 7 nov. 2016
    Implementation of bresenham algorithm
    
    Compute lines between coordinates in 2d or 3d, on hexagonal or square grid
@author: olinox
'''
from math import sqrt
from core.constants import SQUAREGRID, HEXGRID

def line2d(geometry, x1, y1, x2, y2):
    """returns a line from x1,y1 to x2,y2
    grid could be one of the GRIDTYPES values"""
    if not all(isinstance(c, int) for c in [x1, y1, x2, y2]):
        raise TypeError("x1, y1, x2, y2 have to be integers")
    if geometry == SQUAREGRID:
        return _brH(x1, y1, x2, y2)
    elif geometry == HEXGRID: 
        return _brC(x1, y1, x2, y2)
    else:
        raise ValueError("'geometry' has to be a value from GRID_GEOMETRIES")

def line3d(geometry, x1, y1, z1, x2, y2, z2):
    """returns a line from x1,y1,z1 to x2,y2,z2
    grid could be one of the GRIDTYPES values"""
    if not all(isinstance(c, int) for c in [x1, y1, z1, x2, y2, z2]):
        raise TypeError("x1, y1, z1, x2, y2, z2 have to be integers")
    hoLine = line2d(geometry, x1, y1, x2, y2)
    if z1 == z2:
        return [(x, y, z1) for x, y in hoLine]
    else:
        ligneZ = _brC(0, z1, (len(hoLine)-1), z2)
        return [(hoLine[d][0], hoLine[d][1], z) for d, z in ligneZ]

def hex_2d_line(x1, y1, x2, y2):
    """returns a line from x1,y1 to x2,y2 on an hexagonal grid
    line is a list of coordinates"""
    if not all(isinstance(c, int) for c in [x1, y1, x2, y2]):
        raise TypeError("x1, y1, x2, y2 have to be integers")
    if (x1, y1) == (x2, y2):
        return [(x1, y1)]
    return _brH(x1, y1, x2, y2)

def hex_3d_line(x1, y1, z1, x2, y2, z2):
    """returns a line from x1,y1,z1 to x2,y2,z2 on an hexagonal grid
    line is a list of coordinates"""
    if not all(isinstance(c, int) for c in [x1, y1, z1, x2, y2, z2]):
        raise TypeError("x1, y1, z1, x2, y2, z2 have to be integers")
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
    if not all(isinstance(c, int) for c in [x1, y1, x2, y2]):
        raise TypeError("x1, y1, x2, y2 have to be integers")
    if (x1, y1) == (x2, y2):
        return [(x1, y1)]
    return _brC(x1, y1, x2, y2)
    

def squ_3d_line(x1, y1, z1, x2, y2, z2):
    """returns a line from x1,y1,z1 to x2,y2,z2 on an square grid
    line is a list of coordinates"""
    if not all(isinstance(c, int) for c in [x1, y1, z1, x2, y2, z2]):
        raise TypeError("x1, y1, z1, x2, y2, z2 have to be integers")
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