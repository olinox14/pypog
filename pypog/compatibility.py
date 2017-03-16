'''
    Backward compatibility

    ** By Cro-Ki l@b, 2017 **
'''
import math

try:
    inf = math.inf
except AttributeError:
    inf = float("inf")
