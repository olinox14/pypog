'''
Created on 11 dec. 2016

@author: olinox
'''
import unittest

from pypog import geometry


class Test(unittest.TestCase):

    def test_rect_errors(self):
        for method in (geometry.rect, geometry.hollow_rect):
            self.assertRaises( TypeError, method, "a", 1, 1, 1)
            self.assertRaises( TypeError, method, 1, "a", 1, 1)
            self.assertRaises( TypeError, method, 1, 1, "a", 1)
            self.assertRaises( TypeError, method, 1, 1, 1, "a")

    def test_rect(self):
        
        self.assertEquals(geometry.rect(0,0,0,0), [(0,0)])
        self.assertCountEqual(geometry.rect(0,0,1,1), [(0,0), (0,1), (1,1), (1,0)])
        self.assertCountEqual(geometry.rect(1,1,0,0), [(0,0), (0,1), (1,1), (1,0)])
        self.assertCountEqual(geometry.rect(4,3,7,5), [(4, 3), (4, 4), (4, 5), (5, 5), (6, 5), (7, 5), (7, 4), (7, 3), (6, 3), (5, 3), (6, 4), (5, 4)])
        self.assertCountEqual(geometry.rect(3,3,9,9), [(3, 3), (9, 9), (9, 8), (9, 7), (9, 5), (9, 6), (9, 4), (9, 3), (8, 4), (7, 3), (6, 4), (4, 4), 
                                                       (3, 4), (3, 5), (3, 6), (3, 7), (3, 8), (3, 9), (4, 9), (5, 9), (6, 9), (7, 9), (8, 9), (4, 5), 
                                                       (5, 4), (6, 5), (7, 4), (8, 5), (4, 6), (5, 5), (6, 6), (7, 5), (8, 6), (4, 7), (5, 6), (6, 7), 
                                                       (7, 6), (8, 7), (4, 8), (5, 7), (6, 8), (7, 7), (8, 8), (7, 8), (5, 8), (8, 3), (6, 3), (4, 3), 
                                                       (5, 3)])

        self.assertEquals(geometry.hollow_rect(0,0,0,0), [(0,0)])
        self.assertCountEqual(geometry.hollow_rect(0,0,1,1), [(0,0), (0,1), (1,1), (1,0)])
        self.assertCountEqual(geometry.hollow_rect(1,1,0,0), [(0,0), (0,1), (1,1), (1,0)])
        self.assertCountEqual(geometry.hollow_rect(4,3,7,5), [(4, 3), (4, 4), (4, 5), (5, 5), (6, 5), (7, 5), (7, 4), (7, 3), (6, 3), (5, 3)])
        self.assertCountEqual(geometry.hollow_rect(3,3,9,9), [(3, 3), (9, 9), (9, 8), (9, 7), (9, 5), (9, 6), (9, 4), (9, 3), (7, 3), (3, 4), 
                                                              (3, 5), (3, 6), (3, 7), (3, 8), (3, 9), (4, 9), (5, 9), (6, 9), (7, 9), (8, 9), 
                                                              (8, 3), (6, 3), (4, 3), (5, 3)])


if __name__ == "__main__":
    unittest.main()