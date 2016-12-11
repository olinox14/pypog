'''
Created on 22 nov. 2016

@author: olinox
'''
import unittest

from pypog import geometry


class Test(unittest.TestCase):
    """test triangle algorithms"""

    def test_triangle_errors(self):
        
        for cell_shape in (geometry.HEX, geometry.SQUARE):
            self.assertRaises( TypeError, geometry.triangle, cell_shape, "a", 1, 1, 1, 1)
            self.assertRaises( TypeError, geometry.triangle, cell_shape, 1, "a", 1, 1, 1)
            self.assertRaises( TypeError, geometry.triangle, cell_shape, 1, 1, "a", 1, 1)
            self.assertRaises( TypeError, geometry.triangle, cell_shape, 1, 1, 1, "a", 1)
            self.assertRaises( ValueError, geometry.triangle, cell_shape, 1, 1, 1, 1, -1)
    
            self.assertRaises( TypeError, geometry.triangle3d, cell_shape, "a", 1, 1, 1, 1, 1, 1)
            self.assertRaises( TypeError, geometry.triangle3d, cell_shape, 1, "a", 1, 1, 1, 1, 1)
            self.assertRaises( TypeError, geometry.triangle3d, cell_shape, 1, 1, "a", 1, 1, 1, 1)
            self.assertRaises( TypeError, geometry.triangle3d, cell_shape, 1, 1, 1, "a", 1, 1, 1)
            self.assertRaises( TypeError, geometry.triangle3d, cell_shape, 1, 1, 1, 1, "a", 1, 1)
            self.assertRaises( TypeError, geometry.triangle3d, cell_shape, 1, 1, 1, 1, 1, "a", 1)
            self.assertRaises( ValueError, geometry.triangle3d, cell_shape, 1, 1, 1, 1, 1, 1, -1)
            
        self.assertRaises( ValueError, geometry.triangle, 0, 1, 1, 1, 1, 1)
        self.assertRaises( ValueError, geometry.triangle3d, 0, 1, 1, 1, 1, 1, 1, 1)

    def test_sq_triangle(self):
        """test triangle algorithms on square grid"""
        cell_shape = geometry.SQUARE
        
        for i in geometry.ANGLES:
            self.assertCountEqual(geometry.triangle(cell_shape, 0, 0, 0, 0, i), [(0,0)])

        # TODO: check and validate
#         # left to right
#         self.assertCountEqual(geometry.triangle(cell_shape, 2, 3, 4, 3, 1), [])
#         self.assertCountEqual(geometry.triangle(cell_shape, 2, 3, 4, 3, 2), [])
#         self.assertCountEqual(geometry.triangle(cell_shape, 2, 3, 4, 3, 3), [])
#         
#         # top to bottom
#         self.assertCountEqual(geometry.triangle(cell_shape, 2, 3, 4, 3, 2), [])
#         self.assertCountEqual(geometry.triangle(cell_shape, 2, 3, 4, 3, 2), [])
#         self.assertCountEqual(geometry.triangle(cell_shape, 2, 3, 4, 3, 3), [])
#         
#         # right to left
#         self.assertCountEqual(geometry.triangle(cell_shape, 2, 3, 4, 3, 1), [])
#         self.assertCountEqual(geometry.triangle(cell_shape, 2, 3, 4, 3, 2), [])
#         self.assertCountEqual(geometry.triangle(cell_shape, 2, 3, 4, 3, 3), [])
#         
#         # bottom to top
#         self.assertCountEqual(geometry.triangle(cell_shape, 2, 3, 4, 3, 1), [])
#         self.assertCountEqual(geometry.triangle(cell_shape, 2, 3, 4, 3, 2), [])
#         self.assertCountEqual(geometry.triangle(cell_shape, 2, 3, 4, 3, 3), [])
#         
#         # top left to bottom right
#         self.assertCountEqual(geometry.triangle(cell_shape, 2, 3, 4, 3, 1), [])
#         self.assertCountEqual(geometry.triangle(cell_shape, 2, 3, 4, 3, 2), [])
#         self.assertCountEqual(geometry.triangle(cell_shape, 2, 3, 4, 3, 3), [])
#         
#         # bottom right to top left
#         self.assertCountEqual(geometry.triangle(cell_shape, 2, 3, 4, 3, 1), [])
#         self.assertCountEqual(geometry.triangle(cell_shape, 2, 3, 4, 3, 2), [])
#         self.assertCountEqual(geometry.triangle(cell_shape, 2, 3, 4, 3, 3), [])
#         
#         # top right to bottom left
#         self.assertCountEqual(geometry.triangle(cell_shape, 2, 3, 4, 3, 1), [])
#         self.assertCountEqual(geometry.triangle(cell_shape, 2, 3, 4, 3, 2), [])
#         self.assertCountEqual(geometry.triangle(cell_shape, 2, 3, 4, 3, 3), [])
#         
#         # bottom right to top left
#         self.assertCountEqual(geometry.triangle(cell_shape, 2, 3, 4, 3, 1), [])
#         self.assertCountEqual(geometry.triangle(cell_shape, 2, 3, 4, 3, 2), [])
#         self.assertCountEqual(geometry.triangle(cell_shape, 2, 3, 4, 3, 3), [])

        

    def test_hex_triangle(self):
        """test triangle algorithms on hexagonal grid"""
        cell_shape = geometry.HEX
        for i in geometry.ANGLES:
            self.assertCountEqual(geometry.triangle(cell_shape, 0, 0, 0, 0, i), [(0,0)])

        # left to right
        self.assertCountEqual(geometry.triangle(cell_shape, 2, 3, 4, 3, 1), [(3, 3), (3, 4), (3, 3), (4, 5), (4, 4), (4, 3), (4, 2), (4, 1), (4, 1), (3, 1), (3, 2), (2, 3)])
        self.assertCountEqual(geometry.triangle(cell_shape, 2, 3, 4, 3, 2), [(3, 3), (4, 4), (4, 3), (4, 2), (4, 2), (3, 2), (2, 3)])
        self.assertCountEqual(geometry.triangle(cell_shape, 2, 3, 4, 3, 3), [(3, 3), (4, 4), (4, 3), (4, 2), (4, 2), (3, 2), (2, 3)])
        
        # TODO: check and validate
        
#         # top to bottom
#         self.assertCountEqual(geometry.triangle(cell_shape, 2, 3, 4, 3, 1), [])
#         self.assertCountEqual(geometry.triangle(cell_shape, 2, 3, 4, 3, 2), [])
#         self.assertCountEqual(geometry.triangle(cell_shape, 2, 3, 4, 3, 3), [])
#         
        # right to left
        self.assertCountEqual(geometry.triangle(cell_shape, 4, 3, 2, 3, 1), [(3, 2), (3, 1), (3, 2), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 5), (3, 4), (3, 3), (4, 3)])
        self.assertCountEqual(geometry.triangle(cell_shape, 4, 3, 2, 3, 2), [(3, 2), (2, 2), (2, 3), (2, 4), (2, 4), (3, 3), (4, 3)])
        self.assertCountEqual(geometry.triangle(cell_shape, 4, 3, 2, 3, 3), [(3, 2), (2, 2), (2, 3), (2, 4), (2, 4), (3, 3), (4, 3)])
         
#         # bottom to top
#         self.assertCountEqual(geometry.triangle(cell_shape, 2, 3, 4, 3, 1), [])
#         self.assertCountEqual(geometry.triangle(cell_shape, 2, 3, 4, 3, 2), [])
#         self.assertCountEqual(geometry.triangle(cell_shape, 2, 3, 4, 3, 3), [])
#         
#         # top left to bottom right
#         self.assertCountEqual(geometry.triangle(cell_shape, 2, 3, 4, 3, 1), [])
#         self.assertCountEqual(geometry.triangle(cell_shape, 2, 3, 4, 3, 2), [])
#         self.assertCountEqual(geometry.triangle(cell_shape, 2, 3, 4, 3, 3), [])
#         
#         # bottom right to top left
#         self.assertCountEqual(geometry.triangle(cell_shape, 2, 3, 4, 3, 1), [])
#         self.assertCountEqual(geometry.triangle(cell_shape, 2, 3, 4, 3, 2), [])
#         self.assertCountEqual(geometry.triangle(cell_shape, 2, 3, 4, 3, 3), [])
#         
#         # top right to bottom left
#         self.assertCountEqual(geometry.triangle(cell_shape, 2, 3, 4, 3, 1), [])
#         self.assertCountEqual(geometry.triangle(cell_shape, 2, 3, 4, 3, 2), [])
#         self.assertCountEqual(geometry.triangle(cell_shape, 2, 3, 4, 3, 3), [])
#         
#         # bottom right to top left
#         self.assertCountEqual(geometry.triangle(cell_shape, 2, 3, 4, 3, 1), [])
#         self.assertCountEqual(geometry.triangle(cell_shape, 2, 3, 4, 3, 2), [])
#         self.assertCountEqual(geometry.triangle(cell_shape, 2, 3, 4, 3, 3), [])

        
    
    def test_sq_triangle_3d(self):
        """test triangle3d algorithms on square grid"""
        cell_shape = geometry.SQUARE
        #TODO: complete
     
    def test_hex_triangle_3d(self):
        """test triangle3d algorithms on hexagonal grid"""
        cell_shape = geometry.HEX
        #TODO: complete

    def test_errors(self):
        
        for cell_shape in (geometry.HEX, geometry.SQUARE):
            self.assertRaises(ValueError, geometry.triangle, cell_shape, 0, 0, 0, 0, 0)
            self.assertRaises(TypeError, geometry.triangle, cell_shape, "a", 0, 0, 0, 1)
            self.assertRaises(TypeError, geometry.triangle, cell_shape, 0, "a", 0, 0, 1)
            self.assertRaises(TypeError, geometry.triangle, cell_shape, 0, 0, "a", 0, 1)
            self.assertRaises(TypeError, geometry.triangle, cell_shape, 0, 0, 0, "a", 1)
            self.assertRaises(ValueError, geometry.triangle, cell_shape, 0, 0, 0, 0, "a")
    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_sq_triangle']
    unittest.main()