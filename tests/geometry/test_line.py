'''
Created on 20 nov. 2016

@author: olinox
'''
import unittest

from core import geometry
from core.geometry import gline


class Test(unittest.TestCase):
    """test line algorithms"""

    def test_hex_line(self):
        """ 2d line on hexagonal grid """
        grid_shape = geometry.HEX
        line = gline.line2d(grid_shape, 1,1,1,1)
        self.assertEqual(line, [(1,1)])
        
        line = gline.line2d(grid_shape, 0,0,1,1)
        self.assertEqual(line, [(0,0), (0,1), (1,1)])
 
        line = gline.line2d(grid_shape, 0,0,7,3)
        self.assertEqual(line, [(0,0), (1,0), (2,1), (3,1), (4,2), (5,2), (6,3), (7,3)] )
 
        line = gline.line2d(grid_shape, 4,3,0,3)
        self.assertEqual(line, [(4,3), (3,2), (2,3), (1,2), (0,3)] )
 
        line = gline.line2d(grid_shape, 3,0,3,3)
        self.assertEqual(line, [(3,0), (3,1), (3,2), (3,3)] )
 
        
    def test_squ_line(self):
        """ 2d line on square grid """
        grid_shape = geometry.SQUARE
        line = gline.line2d(grid_shape,0,0,0,1)
        self.assertEqual(line, [(0,0), (0,1)])
        
        line = gline.line2d(grid_shape,0,0,1,1)
        self.assertEqual(line, [(0,0), (1,1)])
        
        line = gline.line2d(grid_shape,0,0,7,3)
        self.assertEqual(line, [(0,0), (1,0), (2,1), (3,1), (4,2), (5,2), (6,3), (7,3)] )
 
        line = gline.line2d(grid_shape,4,3,0,3)
        self.assertEqual(line, [(4,3), (3,3), (2,3), (1,3), (0,3)] )
 
        line = gline.line2d(grid_shape,3,0,3,3)
        self.assertEqual(line, [(3,0), (3,1), (3,2), (3,3)] )
    
    def test_hex_line_3d(self):
        """ 3d line on hexagonal grid """
        grid_shape = geometry.HEX
        line = gline.line3d(grid_shape,1,1,1,1,1,1)
        self.assertEqual(line, [(1,1,1)])
    
        line = gline.line3d(grid_shape,1,1,0,1,1,1)
        self.assertEqual(line, [(1,1,0), (1,1,1)])
    
        line = gline.line3d(grid_shape,0,0,0,1,1,1)
        self.assertEqual(line, [(0,0,0), (0,1,0), (1,1,1)])
    
        line = gline.line3d(grid_shape,0,0,0,7,3,7)
        self.assertEqual(line, [(0,0,0), (1,0,1), (2,1,2), (3,1,3), (4,2,4), (5,2,5), (6,3,6), (7,3,7)] )
 
        line = gline.line3d(grid_shape,4,3,10,0,3,3)
        self.assertEqual(line, [(4,3,10), (3,2,9), (3,2,8), (2,3,7), (2,3,6), (1,2,5), (1,2,4), (0,3,3)] )
 
        line = gline.line3d(grid_shape,3,0,0,3,3,0)
        self.assertEqual(line, [(3,0,0), (3,1,0), (3,2,0), (3,3,0)] )
        
    def test_squ_line_3d(self):
        """ 3d line on square grid """
        grid_shape = geometry.SQUARE
        line = gline.line3d(grid_shape,1,1,1,1,1,1)
        self.assertEqual(line, [(1,1,1)])
    
        line = gline.line3d(grid_shape,1,1,0,1,1,1)
        self.assertEqual(line, [(1,1,0), (1,1,1)])
    
        line = gline.line3d(grid_shape,0,0,0,1,1,1)
        self.assertEqual(line, [(0,0,0), (1,1,1)])
    
        line = gline.line3d(grid_shape,0,0,0,7,3,7)
        self.assertEqual(line, [(0,0,0), (1,0,1), (2,1,2), (3,1,3), (4,2,4), (5,2,5), (6,3,6), (7,3,7)] )
 
        line = gline.line3d(grid_shape,4,3,10,0,3,3)
        self.assertEqual(line, [(4,3,10), (3,3,9), (3,3,8), (2,3,7), (2,3,6), (1,3,5), (1,3,4), (0,3,3)] )
 
        line = gline.line3d(grid_shape,3,0,0,3,3,0)
        self.assertEqual(line, [(3,0,0), (3,1,0), (3,2,0), (3,3,0)] )


if __name__ == "__main__":
    unittest.main()