'''
Created on 6 dec. 2016

@author: olinox
'''
import unittest
from pypog import geometry

class Test(unittest.TestCase):

    def test_hex_pivot(self):
        """ pivot on hexagonal grid """
        
        
        attended = [
                    [(5, 5), (4, 5), (6, 6)], 
                    [(5, 6), (4, 7), (6, 6)],
                    [(6, 7), (6, 8), (6, 6)],
                    [(7, 6), (8, 7), (6, 6)],
                    [(7, 5), (8, 5), (6, 6)],
                    [(6, 5), (6, 4), (6, 6)],
                    [(5, 5), (4, 5), (6, 6)]
                   ]
        
        
        for i in range( len(attended) ):
            self.assertCountEqual(geometry.hex_pivot( (6,6), [(6,6)], i), [(6,6)])
            result = geometry.hex_pivot( (6,6), [(5,5), (4,5), (6,6)], i )
            self.assertCountEqual(result, attended[i])
            self.assertCountEqual(result, geometry.pivot(geometry.HEX, (6,6), [(5,5), (4,5), (6,6)], i))

    def test_squ_line(self):
        """ pivot on square grid """
        attended = [
                    [(6, 6), (6, 5), (5, 5), (5, 6)],
                    [(6, 6), (5, 6), (5, 7), (6, 7)],
                    [(6, 6), (6, 7), (7, 7), (7, 6)],
                    [(6, 6), (7, 6), (7, 5), (6, 5)],
                    [(6, 6), (6, 5), (5, 5), (5, 6)]
                   ]

        for i in range( len(attended) ):
            self.assertCountEqual(geometry.hex_pivot( (6,6), [(6,6)], i), [(6,6)])
            result = geometry.squ_pivot( (6,6), [(6,6), (6,5), (5,5), (5,6)], i )
            self.assertCountEqual(result, attended[i])
            self.assertCountEqual(result, geometry.pivot(geometry.SQUARE, (6,6), [(6,6), (6,5), (5,5), (5,6)], i))
     
if __name__ == "__main__":
    unittest.main()