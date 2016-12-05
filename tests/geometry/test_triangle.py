'''
Created on 22 nov. 2016

@author: olinox
'''
import unittest

from pypog import geometry


class Test(unittest.TestCase):
    """test triangle algorithms"""

    def test_sq_triangle(self):
        """test triangle algorithms on square grid"""
        grid_shape = geometry.SQUARE
        
        for i in geometry.ANGLES:
            self.assertCountEqual(geometry.triangle(grid_shape, 0, 0, 0, 0, i), [(0,0)])

        #TODO: complete


    def test_hex_triangle(self):
        """test triangle algorithms on hexagonal grid"""
        grid_shape = geometry.HEX
        for i in geometry.ANGLES:
            self.assertCountEqual(geometry.triangle(grid_shape, 0, 0, 0, 0, i), [(0,0)])
        #TODO: complete
    
    def test_sq_triangle_3d(self):
        """test triangle3d algorithms on square grid"""
        grid_shape = geometry.SQUARE
        #TODO: complete
     
    def test_hex_triangle_3d(self):
        """test triangle3d algorithms on hexagonal grid"""
        grid_shape = geometry.HEX
        #TODO: complete

    def test_errors(self):
        
        for grid_shape in (geometry.HEX, geometry.SQUARE):
            self.assertRaises(ValueError, geometry.triangle, grid_shape, 0, 0, 0, 0, 0)
            self.assertRaises(TypeError, geometry.triangle, grid_shape, "a", 0, 0, 0, 1)
            self.assertRaises(TypeError, geometry.triangle, grid_shape, 0, "a", 0, 0, 1)
            self.assertRaises(TypeError, geometry.triangle, grid_shape, 0, 0, "a", 0, 1)
            self.assertRaises(TypeError, geometry.triangle, grid_shape, 0, 0, 0, "a", 1)
            self.assertRaises(ValueError, geometry.triangle, grid_shape, 0, 0, 0, 0, "a")
    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_sq_triangle']
    unittest.main()