'''
    Graphical functions

    ** By Cro-Ki l@b, 2017 **
'''
from pypog import geometry

def g_cell(shape, *args):
    if shape == geometry.FLAT_HEX:
        return g_flathex(*args)
    elif shape == geometry.SQUARE :
        return g_square(*args)
    else:
        raise geometry.UnknownCellShape()

def g_flathex(x, y, scale=120):
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

def g_square(x, y, scale=120):
    return  [
                (x * scale, y * scale), \
                ((x + 1) * scale, y * scale), \
                ((x + 1) * scale, (y + 1) * scale), \
                (x * scale, (y + 1) * scale)
            ]

