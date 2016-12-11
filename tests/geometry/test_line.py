'''
Created on 20 nov. 2016

@author: olinox
'''
import unittest

from pypog import geometry


class Test(unittest.TestCase):
    """test line algorithms"""

    def test_line_errors(self):
        self.assertRaises( TypeError, geometry.line2d, geometry.HEX, "a", 1, 1, 1)
        self.assertRaises( TypeError, geometry.line2d, geometry.HEX, 1, "a", 1, 1)
        self.assertRaises( TypeError, geometry.line2d, geometry.HEX, 1, 1, "a", 1)
        self.assertRaises( TypeError, geometry.line2d, geometry.HEX, 1, 1, 1, "a")
        self.assertRaises( ValueError, geometry.line2d, 0, 1, 1, 1, 1)

        self.assertRaises( TypeError, geometry.line3d, geometry.HEX, 1, 1, "a", 1, 1, 1)
        self.assertRaises( TypeError, geometry.line3d, geometry.HEX, 1, 1, 1, 1, 1, "a")
        
    def test_line(self):
        """ 2d line on square or hexagonal grid """
        cell_shape = geometry.HEX
        
        attended = {
                    geometry.HEX:    {
                                      (1,1,1,1): [(1,1)], 
                                      (0,0,1,1): [(0,0), (0,1), (1,1)], 
                                      (1,1,0,0): [(1,1), (0,1), (0,0)], 
                                      (0,0,7,3): [(0,0), (1,0), (2,1), (3,1), (4,2), (5,2), (6,3), (7,3)], 
                                      (7,3,0,0): [(7,3), (6,3), (5,2), (4,2), (3,1), (2,1), (1,0), (0,0)], 
                                      (4,3,0,3): [(4,3), (3,2), (2,3), (1,2), (0,3)], 
                                      (0,3,4,3): [(0,3), (1,2), (2,3), (3,2), (4,3)], 
                                      (3,0,3,3): [(3,0), (3,1), (3,2), (3,3)], 
                                      (3,3,3,0): [(3,3), (3,2), (3,1), (3,0)]
                                     }, 
                    
                    geometry.SQUARE: {
                                      (1,1,1,1): [(1,1)], 
                                      (0,0,0,1): [(0,0), (0,1)], 
                                      (0,1,0,0): [(0,1), (0,0)], 
                                      (0,0,1,1): [(0,0), (1,1)], 
                                      (1,1,0,0): [(1,1), (0,0)], 
                                      (0,0,7,3): [(0,0), (1,0), (2,1), (3,1), (4,2), (5,2), (6,3), (7,3)], 
                                      (7,3,0,0): [(7,3), (6,3), (5,2), (4,2), (3,1), (2,1), (1,0), (0,0)], 
                                      (4,3,0,3): [(4,3), (3,3), (2,3), (1,3), (0,3)], 
                                      (0,3,4,3): [(0,3), (1,3), (2,3), (3,3), (4,3)], 
                                      (3,0,3,3): [(3,0), (3,1), (3,2), (3,3)],                      
                                      (3,3,3,0): [(3,3), (3,2), (3,1), (3,0)]                    
                                     }
                   }
        
        for cell_shape, tests in attended.items():
            for args, result in tests.items():
                line = geometry.line2d(cell_shape, *args)
                self.assertEqual(line, result)
        
    
    def test_line_3d(self):
        """ 3d line on hexagonal and square grid """
        cell_shape = geometry.HEX
        
        attended = {
                    geometry.HEX:    {
                                      (1,1,1,1,1,1) : [(1,1,1)], 
                                      (1,1,0,1,1,1) : [(1,1,0), (1,1,1)], 
                                      (0,0,0,1,1,1) : [(0,0,0), (0,1,0), (1,1,1)], 
                                      (0,0,0,7,3,7) : [(0,0,0), (1,0,1), (2,1,2), (3,1,3), (4,2,4), (5,2,5), (6,3,6), (7,3,7)], 
                                      (4,3,10,0,3,3): [(4,3,10), (3,2,9), (3,2,8), (2,3,7), (2,3,6), (1,2,5), (1,2,4), (0,3,3)], 
                                      (3,0,0,3,3,0) : [(3,0,0), (3,1,0), (3,2,0), (3,3,0)]
                                     }, 
                    
                    geometry.SQUARE: {
                                      (1,1,1,1,1,1) : [(1,1,1)], 
                                      (1,1,0,1,1,1) : [(1,1,0), (1,1,1)], 
                                      (0,0,0,1,1,1) : [(0,0,0), (1,1,1)], 
                                      (0,0,0,7,3,7) : [(0,0,0), (1,0,1), (2,1,2), (3,1,3), (4,2,4), (5,2,5), (6,3,6), (7,3,7)], 
                                      (4,3,10,0,3,3): [(4,3,10), (3,3,9), (3,3,8), (2,3,7), (2,3,6), (1,3,5), (1,3,4), (0,3,3)], 
                                      (3,0,0,3,3,0) : [(3,0,0), (3,1,0), (3,2,0), (3,3,0)]
                                     }
                   }
        
        for cell_shape, tests in attended.items():
            for args, result in tests.items():
                line = geometry.line3d(cell_shape, *args)
                self.assertEqual(line, result)
        

if __name__ == "__main__":
    unittest.main()