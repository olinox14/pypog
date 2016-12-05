'''
Created on 25 nov. 2016

@author: olinox
'''
import unittest

from pypog import geometry


class Test(unittest.TestCase):


    def test_neighbours_of(self):
        for coord in ( (0,0), (-10,-10), (10,10) ):
            x, y = coord
            self.assertEqual( geometry.neighbours_of(geometry.HEX, x, y), geometry.hex_neighbours_of(x, y) )
            self.assertEqual( geometry.neighbours_of(geometry.SQUARE, x, y), geometry.squ_neighbours_of(x, y) )

    def test_hex_neighbours_of(self):
        self.assertCountEqual( geometry.hex_neighbours_of(3,3), [(3,2), (4,3), (4,4), (3,4), (2,4), (2,3)] )
        self.assertCountEqual( geometry.hex_neighbours_of(4,4), [(4,3), (5,3), (5,4), (4,5), (3,4), (3,3)] )

    def test_squ_neighbours_of(self):
        self.assertCountEqual( geometry.squ_neighbours_of(3,3), [(2,3), (2,2), (3,2), (4,2), (4,3), (4,4), (3,4), (2,4)] )
        

if __name__ == "__main__":
    unittest.main()