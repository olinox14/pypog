'''
Created on 20 nov. 2016

@author: olinox
'''
import unittest

from pypog import geometry



class Test(unittest.TestCase):
    """ test the zone algorithm """


    def test_hex_zone(self):
        """ test the zone algo for hexagonal grid """
        cell_shape = geometry.HEX
        self.assertCountEqual( geometry.zone( cell_shape, 3, 3, 0 ), [(3,3)])
        self.assertCountEqual( geometry.zone( cell_shape, 3, 3, 1 ), [(3, 2), (2, 3), (3, 3), (4, 3), (4, 4), (3, 4), (2, 4)])
        self.assertCountEqual( geometry.zone( cell_shape, 3, 3, 2 ), [(3, 2), (1, 3), (5, 4), (4, 5), (1, 4), (2, 3), (4, 2), \
                                                            (2, 5), (5, 3), (1, 2), (3, 5), (3, 3), (4, 4), (3, 1), \
                                                            (4, 3), (2, 2), (3, 4), (2, 4), (5, 2)] )

    def test_squ_zone(self):
        """ test the zone algo for square grid """
        cell_shape = geometry.SQUARE
        self.assertCountEqual( geometry.zone( cell_shape, 3, 3, 0 ), [(3,3)])
        self.assertCountEqual( geometry.zone( cell_shape, 3, 3, 1 ), [(3, 2), (3, 3), (4, 4), (2, 3), (4, 3), (2, 2), (4, 2), (3, 4), (2, 4)])
        self.assertCountEqual( geometry.zone( cell_shape, 3, 3, 2 ), [(2, 4), (3, 2), (5, 4), (1, 3), (4, 5), (2, 1), (1, 4), (2, 3), (4, 2), \
                                                                    (5, 1), (2, 5), (3, 5), (5, 3), (1, 2), (3, 3), (5, 5), (4, 4), (3, 1), \
                                                                    (1, 5), (4, 3), (2, 2), (4, 1), (5, 2), (3, 4), (1, 1)])

    def test_errors(self):
        """test the errors due to bad parameters"""
        self.assertRaises( TypeError, geometry.zone, 5, 0, 0, "a")
        self.assertRaises( TypeError, geometry.zone, 5, "a", 0, 1)
        self.assertRaises( TypeError, geometry.zone, 5, 0, "a", 1)
        self.assertRaises( ValueError, geometry.zone, 5, 0, 0, -1)
        self.assertRaises( ValueError, geometry.zone, -1, 0, 0, 1)
        self.assertRaises( ValueError, geometry.zone, "a", 0, 0, 1)

if __name__ == "__main__":
    unittest.main()