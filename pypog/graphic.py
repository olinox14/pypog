'''
Created on 5 dec. 2016

@author: olinox
'''

from pypog import geometry


def polygon(shape, x, y, scale = 120):
    if shape == geometry.HEX:
        
        if 1 == (x % 2): 
            y += 0.5
            
        return [
                   ( ((x*0.866)+0.2886) * scale ,   y * scale), \
                   ( ((x*0.866)+0.866) * scale  ,   y * scale), \
                   ( ((x*0.866)+1.1547) * scale ,   (y+0.5) * scale), \
                   ( ((x*0.866)+0.866) * scale  ,   (y+1) * scale), \
                   ( ((x*0.866)+0.2886) * scale ,   (y+1) * scale),  \
                   ( (x*0.866) * scale          ,   (y+0.5) * scale) 
                ]

    elif shape == geometry.SQUARE :
        
        return  [ 
                    (x * scale,      y * scale), \
                    ((x+1) * scale,  y * scale), \
                    ((x+1) * scale,  (y+1) * scale), \
                    (x * scale,       (y+1) * scale) 
                ]   
        
    else:
        raise ValueError("'shape' has to be a value from GEOMETRIES")
