'''

    ** By Cro-Ki l@b, 2017 **
'''
import unittest

from pypog import geometry


class Test(unittest.TestCase):

    def test_line_errors(self):
        self.assertRaises(TypeError, geometry.line2d, geometry.FLAT_HEX, "a", 1, 1, 1)
        self.assertRaises(TypeError, geometry.line2d, geometry.FLAT_HEX, 1, "a", 1, 1)
        self.assertRaises(TypeError, geometry.line2d, geometry.FLAT_HEX, 1, 1, "a", 1)
        self.assertRaises(TypeError, geometry.line2d, geometry.FLAT_HEX, 1, 1, 1, "a")
        self.assertRaises(ValueError, geometry.line2d, 0, 1, 1, 1, 1)

        self.assertRaises(TypeError, geometry.line3d, geometry.FLAT_HEX, 1, 1, "a", 1, 1, 1)
        self.assertRaises(TypeError, geometry.line3d, geometry.FLAT_HEX, 1, 1, 1, 1, 1, "a")

    def test_line2d(self):
        """ 2d line on square or hexagonal grid """
        cell_shape = geometry.FLAT_HEX

        attended = {
                    geometry.FLAT_HEX:    {
                                      (1, 1, 1, 1): [(1, 1)],
                                      (0, 0, 1, 1): [(0, 0), (0, 1), (1, 1)],
                                      (1, 1, 0, 0): [(1, 1), (0, 1), (0, 0)],
                                      (0, 0, 7, 3): [(0, 0), (1, 0), (2, 1), (3, 1), (4, 2), (5, 2), (6, 3), (7, 3)],
                                      (7, 3, 0, 0): [(7, 3), (6, 3), (5, 2), (4, 2), (3, 1), (2, 1), (1, 0), (0, 0)],
                                      (4, 3, 0, 3): [(4, 3), (3, 2), (2, 3), (1, 2), (0, 3)],
                                      (0, 3, 4, 3): [(0, 3), (1, 2), (2, 3), (3, 2), (4, 3)],
                                      (3, 0, 3, 3): [(3, 0), (3, 1), (3, 2), (3, 3)],
                                      (3, 3, 3, 0): [(3, 3), (3, 2), (3, 1), (3, 0)]
                                     },

                    geometry.SQUARE: {
                                      (1, 1, 1, 1): [(1, 1)],
                                      (0, 0, 0, 1): [(0, 0), (0, 1)],
                                      (0, 1, 0, 0): [(0, 1), (0, 0)],
                                      (0, 0, 1, 1): [(0, 0), (1, 1)],
                                      (1, 1, 0, 0): [(1, 1), (0, 0)],
                                      (0, 0, 7, 3): [(0, 0), (1, 0), (2, 1), (3, 1), (4, 2), (5, 2), (6, 3), (7, 3)],
                                      (7, 3, 0, 0): [(7, 3), (6, 3), (5, 2), (4, 2), (3, 1), (2, 1), (1, 0), (0, 0)],
                                      (4, 3, 0, 3): [(4, 3), (3, 3), (2, 3), (1, 3), (0, 3)],
                                      (0, 3, 4, 3): [(0, 3), (1, 3), (2, 3), (3, 3), (4, 3)],
                                      (3, 0, 3, 3): [(3, 0), (3, 1), (3, 2), (3, 3)],
                                      (3, 3, 3, 0): [(3, 3), (3, 2), (3, 1), (3, 0)]
                                     }
                   }

        for cell_shape, tests in attended.items():
            for args, result in tests.items():
                line = geometry.line2d(cell_shape, *args)
                self.assertEqual(line, result)

    def test_line3d(self):
        """ 3d line on hexagonal and square grid """
        cell_shape = geometry.FLAT_HEX

        attended = {
                    geometry.FLAT_HEX:    {
                                      (1, 1, 1, 1, 1, 1) : [(1, 1, 1)],
                                      (1, 1, 0, 1, 1, 1) : [(1, 1, 0), (1, 1, 1)],
                                      (0, 0, 0, 1, 1, 1) : [(0, 0, 0), (0, 1, 0), (1, 1, 1)],
                                      (0, 0, 0, 7, 3, 7) : [(0, 0, 0), (1, 0, 1), (2, 1, 2), (3, 1, 3), (4, 2, 4), (5, 2, 5), (6, 3, 6), (7, 3, 7)],
                                      (4, 3, 10, 0, 3, 3): [(4, 3, 10), (3, 2, 9), (3, 2, 8), (2, 3, 7), (2, 3, 6), (1, 2, 5), (1, 2, 4), (0, 3, 3)],
                                      (3, 0, 0, 3, 3, 0) : [(3, 0, 0), (3, 1, 0), (3, 2, 0), (3, 3, 0)]
                                     },

                    geometry.SQUARE: {
                                      (1, 1, 1, 1, 1, 1) : [(1, 1, 1)],
                                      (1, 1, 0, 1, 1, 1) : [(1, 1, 0), (1, 1, 1)],
                                      (0, 0, 0, 1, 1, 1) : [(0, 0, 0), (1, 1, 1)],
                                      (0, 0, 0, 7, 3, 7) : [(0, 0, 0), (1, 0, 1), (2, 1, 2), (3, 1, 3), (4, 2, 4), (5, 2, 5), (6, 3, 6), (7, 3, 7)],
                                      (4, 3, 10, 0, 3, 3): [(4, 3, 10), (3, 3, 9), (3, 3, 8), (2, 3, 7), (2, 3, 6), (1, 3, 5), (1, 3, 4), (0, 3, 3)],
                                      (3, 0, 0, 3, 3, 0) : [(3, 0, 0), (3, 1, 0), (3, 2, 0), (3, 3, 0)]
                                     }
                   }

        for cell_shape, tests in attended.items():
            for args, result in tests.items():
                line = geometry.line3d(cell_shape, *args)
                self.assertEqual(line, result)

    def test_neighbours(self):
        for coord in ((0, 0), (-10, -10), (10, 10)):
            x, y = coord
            self.assertEqual(geometry.neighbours(geometry.FLAT_HEX, x, y), geometry.fhex_neighbours(x, y))
            self.assertEqual(geometry.neighbours(geometry.SQUARE, x, y), geometry.squ_neighbours(x, y))

    def test_fhex_neighbours(self):
        self.assertCountEqual(geometry.fhex_neighbours(3, 3), [(3, 2), (4, 3), (4, 4), (3, 4), (2, 4), (2, 3)])
        self.assertCountEqual(geometry.fhex_neighbours(4, 4), [(4, 3), (5, 3), (5, 4), (4, 5), (3, 4), (3, 3)])

    def test_squ_neighbours(self):
        self.assertCountEqual(geometry.squ_neighbours(3, 3), [(2, 3), (2, 2), (3, 2), (4, 2), (4, 3), (4, 4), (3, 4), (2, 4)])

    def test_pivot_errors(self):

        # invalid cell shape
        self.assertRaises(ValueError, geometry.pivot, 0, (0, 0), [(0, 0)], 1)

        self.assertRaises(TypeError, geometry.pivot, 0, "a"    , [(0, 0)], 1)
        self.assertRaises(ValueError, geometry.pivot, 0, ("a", 0), [(0, 0)], 1)

        self.assertRaises(TypeError, geometry.pivot, 0, (0, 0), 0, 1)
        self.assertRaises(ValueError, geometry.pivot, 0, (0, 0), ["a", (0, 0)], 1)
        self.assertRaises(ValueError, geometry.pivot, 0, (0, 0), [("a", 0), (0, 0)], 1)

        self.assertRaises(TypeError, geometry.pivot, 0, (0, 0), 1, "a")

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


        for i in range(len(attended)):
            self.assertCountEqual(geometry.pivot(geometry.FLAT_HEX, (6, 6), [(6, 6)], i), [(6, 6)])
            result = geometry.pivot(geometry.FLAT_HEX, (6, 6), [(5, 5), (4, 5), (6, 6)], i)
            self.assertCountEqual(result, attended[i])

    def test_squ_pivot(self):
        """ pivot on square grid """
        attended = [
                    [(6, 6), (6, 5), (5, 5), (5, 6)],
                    [(6, 6), (5, 6), (5, 7), (6, 7)],
                    [(6, 6), (6, 7), (7, 7), (7, 6)],
                    [(6, 6), (7, 6), (7, 5), (6, 5)],
                    [(6, 6), (6, 5), (5, 5), (5, 6)]
                   ]

        for i in range(len(attended)):
            self.assertCountEqual(geometry.pivot(geometry.SQUARE, (6, 6), [(6, 6)], i), [(6, 6)])
            result = geometry.pivot(geometry.SQUARE, (6, 6), [(6, 6), (6, 5), (5, 5), (5, 6)], i)
            self.assertCountEqual(result, attended[i])


    def test_rectangle_errors(self):
        for method in (geometry.rectangle, geometry.hollow_rectangle):
            self.assertRaises(TypeError, method, "a", 1, 1, 1)
            self.assertRaises(TypeError, method, 1, "a", 1, 1)
            self.assertRaises(TypeError, method, 1, 1, "a", 1)
            self.assertRaises(TypeError, method, 1, 1, 1, "a")

    def test_rectangle(self):

        self.assertEquals(geometry.rectangle(0, 0, 0, 0), [(0, 0)])
        self.assertCountEqual(geometry.rectangle(0, 0, 1, 1), [(0, 0), (0, 1), (1, 1), (1, 0)])
        self.assertCountEqual(geometry.rectangle(1, 1, 0, 0), [(0, 0), (0, 1), (1, 1), (1, 0)])
        self.assertCountEqual(geometry.rectangle(4, 3, 7, 5), [(4, 3), (4, 4), (4, 5), (5, 5), (6, 5), (7, 5), (7, 4), (7, 3), (6, 3), (5, 3), (6, 4), (5, 4)])
        self.assertCountEqual(geometry.rectangle(3, 3, 9, 9), [(3, 3), (9, 9), (9, 8), (9, 7), (9, 5), (9, 6), (9, 4), (9, 3), (8, 4), (7, 3), (6, 4), (4, 4),
                                                       (3, 4), (3, 5), (3, 6), (3, 7), (3, 8), (3, 9), (4, 9), (5, 9), (6, 9), (7, 9), (8, 9), (4, 5),
                                                       (5, 4), (6, 5), (7, 4), (8, 5), (4, 6), (5, 5), (6, 6), (7, 5), (8, 6), (4, 7), (5, 6), (6, 7),
                                                       (7, 6), (8, 7), (4, 8), (5, 7), (6, 8), (7, 7), (8, 8), (7, 8), (5, 8), (8, 3), (6, 3), (4, 3),
                                                       (5, 3)])

        self.assertEquals(geometry.hollow_rectangle(0, 0, 0, 0), [(0, 0)])
        self.assertCountEqual(geometry.hollow_rectangle(0, 0, 1, 1), [(0, 0), (0, 1), (1, 1), (1, 0)])
        self.assertCountEqual(geometry.hollow_rectangle(1, 1, 0, 0), [(0, 0), (0, 1), (1, 1), (1, 0)])
        self.assertCountEqual(geometry.hollow_rectangle(4, 3, 7, 5), [(4, 3), (4, 4), (4, 5), (5, 5), (6, 5), (7, 5), (7, 4), (7, 3), (6, 3), (5, 3)])
        self.assertCountEqual(geometry.hollow_rectangle(3, 3, 9, 9), [(3, 3), (9, 9), (9, 8), (9, 7), (9, 5), (9, 6), (9, 4), (9, 3), (7, 3), (3, 4),
                                                              (3, 5), (3, 6), (3, 7), (3, 8), (3, 9), (4, 9), (5, 9), (6, 9), (7, 9), (8, 9),
                                                              (8, 3), (6, 3), (4, 3), (5, 3)])

    def test_triangle_errors(self):

        for cell_shape in (geometry.FLAT_HEX, geometry.SQUARE):
            self.assertRaises(TypeError, geometry.triangle, cell_shape, "a", 1, 1, 1, 1)
            self.assertRaises(TypeError, geometry.triangle, cell_shape, 1, "a", 1, 1, 1)
            self.assertRaises(TypeError, geometry.triangle, cell_shape, 1, 1, "a", 1, 1)
            self.assertRaises(TypeError, geometry.triangle, cell_shape, 1, 1, 1, "a", 1)
            self.assertRaises(ValueError, geometry.triangle, cell_shape, 1, 1, 1, 1, -1)

            self.assertRaises(TypeError, geometry.triangle3d, cell_shape, "a", 1, 1, 1, 1, 1, 1)
            self.assertRaises(TypeError, geometry.triangle3d, cell_shape, 1, "a", 1, 1, 1, 1, 1)
            self.assertRaises(TypeError, geometry.triangle3d, cell_shape, 1, 1, "a", 1, 1, 1, 1)
            self.assertRaises(TypeError, geometry.triangle3d, cell_shape, 1, 1, 1, "a", 1, 1, 1)
            self.assertRaises(TypeError, geometry.triangle3d, cell_shape, 1, 1, 1, 1, "a", 1, 1)
            self.assertRaises(TypeError, geometry.triangle3d, cell_shape, 1, 1, 1, 1, 1, "a", 1)
            self.assertRaises(ValueError, geometry.triangle3d, cell_shape, 1, 1, 1, 1, 1, 1, -1)

        self.assertRaises(ValueError, geometry.triangle, 0, 1, 1, 1, 1, 1)
        self.assertRaises(ValueError, geometry.triangle3d, 0, 1, 1, 1, 1, 1, 1, 1)

    def test_squ2_triangle(self):
        """test triangle algorithms on square grid"""
        cell_shape = geometry.SQUARE

        for i in geometry.ANGLES:
            self.assertCountEqual(geometry.triangle(cell_shape, 0, 0, 0, 0, i), [(0, 0)])

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



    def test_fhex2_triangle(self):
        """test triangle algorithms on hexagonal grid"""
        cell_shape = geometry.FLAT_HEX
        for i in geometry.ANGLES:
            self.assertCountEqual(geometry.triangle(cell_shape, 0, 0, 0, 0, i), [(0, 0)])

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



    def test_squ3_triangle(self):
        """test triangle3d algorithms on square grid"""
        cell_shape = geometry.SQUARE
        # TODO: complete

    def test_fhex3_triangle(self):
        """test triangle3d algorithms on hexagonal grid"""
        cell_shape = geometry.FLAT_HEX
        # TODO: complete

    def test_zone(self):
        """test the errors due to bad parameters"""
        self.assertRaises(TypeError, geometry.zone, 5, 0, 0, "a")
        self.assertRaises(TypeError, geometry.zone, 5, "a", 0, 1)
        self.assertRaises(TypeError, geometry.zone, 5, 0, "a", 1)
        self.assertRaises(ValueError, geometry.zone, 5, 0, 0, -1)
        self.assertRaises(ValueError, geometry.zone, -1, 0, 0, 1)
        self.assertRaises(ValueError, geometry.zone, "a", 0, 0, 1)

    def test_hex_zone(self):
        """ test the zone algo for hexagonal grid """
        cell_shape = geometry.FLAT_HEX
        self.assertCountEqual(geometry.zone(cell_shape, 3, 3, 0), [(3, 3)])
        self.assertCountEqual(geometry.zone(cell_shape, 3, 3, 1), [(3, 2), (2, 3), (3, 3), (4, 3), (4, 4), (3, 4), (2, 4)])
        self.assertCountEqual(geometry.zone(cell_shape, 3, 3, 2), [(3, 2), (1, 3), (5, 4), (4, 5), (1, 4), (2, 3), (4, 2), \
                                                            (2, 5), (5, 3), (1, 2), (3, 5), (3, 3), (4, 4), (3, 1), \
                                                            (4, 3), (2, 2), (3, 4), (2, 4), (5, 2)])

    def test_squ_zone(self):
        """ test the zone algo for square grid """
        cell_shape = geometry.SQUARE
        self.assertCountEqual(geometry.zone(cell_shape, 3, 3, 0), [(3, 3)])
        self.assertCountEqual(geometry.zone(cell_shape, 3, 3, 1), [(3, 2), (3, 3), (4, 4), (2, 3), (4, 3), (2, 2), (4, 2), (3, 4), (2, 4)])
        self.assertCountEqual(geometry.zone(cell_shape, 3, 3, 2), [(2, 4), (3, 2), (5, 4), (1, 3), (4, 5), (2, 1), (1, 4), (2, 3), (4, 2), \
                                                                    (5, 1), (2, 5), (3, 5), (5, 3), (1, 2), (3, 3), (5, 5), (4, 4), (3, 1), \
                                                                    (1, 5), (4, 3), (2, 2), (4, 1), (5, 2), (3, 4), (1, 1)])

if __name__ == "__main__":
    unittest.main()
