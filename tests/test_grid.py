'''
Created on 20 nov. 2016

@author: olinox
'''
import unittest

from core import geometry
from core.Grid import Grid, SquareGrid, HexGrid


class Test(unittest.TestCase):

    def test_init(self):
        #square grid
        _ = Grid( geometry.SQUARE, 1, 1 )
        _ = SquareGrid( 1, 1 )
        
        #hex grid
        _ = Grid( geometry.HEX, 1, 1 )
        _ = HexGrid( 1, 1 )

    def test_geometry(self):
        grid = Grid( geometry.SQUARE, 1, 1 )
        self.assertEqual( grid.geometry, geometry.SQUARE )
        
        grid.geometry = geometry.HEX
        self.assertEqual( grid.geometry, geometry.HEX )

        def _set_invalid_geometry():
            grid.geometry = -1
        self.assertRaises( ValueError, _set_invalid_geometry )

    def test_dimensions(self):
        
        for cls in (SquareGrid, HexGrid):
            grid = cls( 1, 1 )
            self.assertEqual( grid.height, 1 )
            self.assertEqual( grid.width, 1 )
    
            grid.height = 1000
            self.assertEqual( grid.height, 1000 )
            grid.width = 1000
            self.assertEqual( grid.width, 1000 )
    
            def _set_invalid_height():
                grid.height = -1
            self.assertRaises( ValueError, _set_invalid_height )
            
            def _set_invalid_width():
                grid.height = -1
            self.assertRaises( ValueError, _set_invalid_width )
        
    def test_cases_number(self):
        for cls in (SquareGrid, HexGrid):
            grid = cls( 1, 1 )
            self.assertEqual( grid.cases_number(), 1 )
            
            grid.width = 100
            grid.height = 100
            
            self.assertEqual( grid.cases_number(), 10000 )
    
    def test_in_grid(self):
        
        for cls in (SquareGrid, HexGrid):
            grid = cls( 10, 10 )
            self.assertTrue( grid.in_grid(5, 5) )
            self.assertFalse( grid.in_grid(11, 5) )
            self.assertFalse( grid.in_grid(5, 11) )

    def test_line(self):
         
        #line algorithm is tested in tests.geometry.test_line
        
        grid = SquareGrid(10, 10)
         
        line = grid.line(0,0,0,1)
        self.assertEqual(line, [(0,0), (0,1)])
        
    def test_line_3d(self):
        
        #line algorithm is tested in tests.geometry.test_line
        
        grid = HexGrid(10, 10)
    
        line = grid.line3d(1,1,1,1,1,1)
        self.assertEqual(line, [(1,1,1)])
    

    def test_hex_zone(self):
        
        #zone algorithm is tested in tests.geometry.test_zone
        
        grid = HexGrid(10,10)
        zone = grid.zone( 0, 0, 0 )
        self.assertCountEqual(zone, [(0,0)])


if __name__ == "__main__":
    unittest.main()