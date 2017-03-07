'''

    Tests for 'geometry' module

    ** By Cro-Ki l@b, 2017 **
'''
from math import inf
import unittest

from pypog.geometry_objects import FHexGeometry, SquareGeometry, BaseGeometry, \
    BoundingRect, IBoundingRect


class Test(unittest.TestCase):

    def setUp(self):
        SquareGeometry.set_no_diagonals(False)

    def test_bounding_rect(self):
        br = BoundingRect(0, 1, 10, 11)
        self.assertEqual(br.xmin, 0)
        self.assertEqual(br.ymin, 1)
        self.assertEqual(br.xmax, 10)
        self.assertEqual(br.ymax, 11)
        self.assertEqual(br.topleft, (0, 1))
        self.assertEqual(br.bottomright, (10, 11))
        self.assertEqual(br.width, 11)
        self.assertEqual(br.height, 11)
        self.assertTrue((5, 5) in br)
        self.assertFalse((15, 15) in br)

        ibr = IBoundingRect()
        self.assertTrue((5, 5) in ibr)
        self.assertTrue((15, 15) in ibr)
        self.assertTrue((10000, 10000) in ibr)
        self.assertEqual(ibr.xmin, -inf)
        self.assertEqual(ibr.ymin, -inf)
        self.assertEqual(ibr.xmax, inf)
        self.assertEqual(ibr.ymax, inf)
        self.assertEqual(ibr.topleft, (-inf, -inf))
        self.assertEqual(ibr.bottomright, (inf, inf))
        self.assertEqual(ibr.width, inf)
        self.assertEqual(ibr.height, inf)

    def test_various(self):
        self.assertEqual(str(BaseGeometry()), "<BaseGeometry object>")
        self.assertEqual(str(SquareGeometry()), "<SquareGeometry object>")
        self.assertEqual(str(FHexGeometry()), "<FHexGeometry object>")

        self.assertTrue(isinstance(BaseGeometry.instance(), BaseGeometry))

        self.assertRaises(NotImplementedError, BaseGeometry.graphicsitem, 0, 0, 120)
        self.assertRaises(NotImplementedError, BaseGeometry.neighbors, 0, 0)
        self.assertRaises(NotImplementedError, BaseGeometry.line, 0, 0, 0, 0)
        self.assertRaises(NotImplementedError, BaseGeometry.triangle, 0, 0, 0, 0, 1)
        self.assertRaises(NotImplementedError, BaseGeometry.triangle3d, 0, 0, 0, 0, 0, 0, 1)
        self.assertRaises(NotImplementedError, BaseGeometry.rotate, (0, 0), [(0, 0)], 1)


    # # neighbors
    def test_neighbors(self):
        """ test for geometry.neighbors """
        self.assertCountEqual(FHexGeometry.neighbors(3, 3), [(3, 2), (4, 3), (4, 4), (3, 4), (2, 4), (2, 3)])
        self.assertCountEqual(FHexGeometry.neighbors(4, 4), [(4, 3), (5, 3), (5, 4), (4, 5), (3, 4), (3, 3)])

        self.assertCountEqual(SquareGeometry.neighbors(3, 3), [(2, 3), (2, 2), (3, 2), (4, 2), (4, 3), (4, 4), (3, 4), (2, 4)])
        SquareGeometry.set_no_diagonals(True)
        self.assertCountEqual(SquareGeometry.neighbors(3, 3), [(2, 3), (3, 2), (4, 3), (3, 4)])

    def test_zone(self):
        """ test for geometry.zone """
        self.assertRaises(ValueError, BaseGeometry.zone, "a", 0, 1)
        self.assertRaises(ValueError, BaseGeometry.zone, 0, "a", 1)
        self.assertRaises(ValueError, BaseGeometry.zone, 0, 0, "a")
        self.assertRaises(ValueError, BaseGeometry.zone, 0, 0, -1)

        self.assertCountEqual(FHexGeometry.zone(3, 3, 0), [(3, 3)])
        self.assertCountEqual(FHexGeometry.zone(3, 3, 1), [(3, 2), (2, 3), (3, 3), (4, 3), (4, 4), (3, 4), (2, 4)])
        self.assertCountEqual(FHexGeometry.zone(3, 3, 2), [(3, 2), (1, 3), (5, 4), (4, 5), (1, 4), (2, 3), (4, 2), \
                                                            (2, 5), (5, 3), (1, 2), (3, 5), (3, 3), (4, 4), (3, 1), \
                                                            (4, 3), (2, 2), (3, 4), (2, 4), (5, 2)])

        self.assertCountEqual(SquareGeometry.zone(3, 3, 0), [(3, 3)])
        self.assertCountEqual(SquareGeometry.zone(3, 3, 1), [(3, 2), (3, 3), (4, 4), (2, 3), (4, 3), (2, 2), (4, 2), (3, 4), (2, 4)])
        self.assertCountEqual(SquareGeometry.zone(3, 3, 2), [(2, 4), (3, 2), (5, 4), (1, 3), (4, 5), (2, 1), (1, 4), (2, 3), (4, 2), \
                                                                (5, 1), (2, 5), (3, 5), (5, 3), (1, 2), (3, 3), (5, 5), (4, 4), (3, 1), \
                                                                (1, 5), (4, 3), (2, 2), (4, 1), (5, 2), (3, 4), (1, 1)])

    # # lines

    def test_line2d(self):
        """ test for geometry.line """
        for geometry in (SquareGeometry, FHexGeometry):
            self.assertRaises(ValueError, geometry.line, "a", 1, 1, 1)
            self.assertRaises(ValueError, geometry.line, 1, "a", 1, 1)
            self.assertRaises(ValueError, geometry.line, 1, 1, "a", 1)
            self.assertRaises(ValueError, geometry.line, 1, 1, 1, "a")

        attended = {
                    FHexGeometry:    {
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

                    SquareGeometry: {
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

        for geometry, tests in attended.items():
            for args, attended in tests.items():
                result = geometry.line(*args)
                self.assertCountEqual(result, attended)

    def test_line3d(self):
        """ test for geometry.line3d """
        for geometry in (SquareGeometry, FHexGeometry):
            self.assertRaises(ValueError, geometry.line3d, 1, 1, "a", 1, 1, 1)
            self.assertRaises(ValueError, geometry.line3d, 1, 1, 1, 1, 1, "a")

        attended = {
                    FHexGeometry:    {
                                      (1, 1, 1, 1, 1, 1) : [(1, 1, 1)],
                                      (1, 1, 0, 1, 1, 1) : [(1, 1, 0), (1, 1, 1)],
                                      (0, 0, 0, 1, 1, 1) : [(0, 0, 0), (0, 1, 0), (1, 1, 1)],
                                      (0, 0, 0, 7, 3, 7) : [(0, 0, 0), (1, 0, 1), (2, 1, 2), (3, 1, 3), (4, 2, 4), (5, 2, 5), (6, 3, 6), (7, 3, 7)],
                                      (4, 3, 10, 0, 3, 3): [(4, 3, 10), (3, 2, 9), (3, 2, 8), (2, 3, 7), (2, 3, 6), (1, 2, 5), (1, 2, 4), (0, 3, 3)],
                                      (3, 0, 0, 3, 3, 0) : [(3, 0, 0), (3, 1, 0), (3, 2, 0), (3, 3, 0)]
                                     },

                    SquareGeometry: {
                                      (1, 1, 1, 1, 1, 1) : [(1, 1, 1)],
                                      (1, 1, 0, 1, 1, 1) : [(1, 1, 0), (1, 1, 1)],
                                      (0, 0, 0, 1, 1, 1) : [(0, 0, 0), (1, 1, 1)],
                                      (0, 0, 0, 7, 3, 7) : [(0, 0, 0), (1, 0, 1), (2, 1, 2), (3, 1, 3), (4, 2, 4), (5, 2, 5), (6, 3, 6), (7, 3, 7)],
                                      (4, 3, 10, 0, 3, 3): [(4, 3, 10), (3, 3, 9), (3, 3, 8), (2, 3, 7), (2, 3, 6), (1, 3, 5), (1, 3, 4), (0, 3, 3)],
                                      (3, 0, 0, 3, 3, 0) : [(3, 0, 0), (3, 1, 0), (3, 2, 0), (3, 3, 0)]
                                     }
                   }

        for geometry, tests in attended.items():
            for args, result in tests.items():
                line = geometry.line3d(*args)
                self.assertEqual(line, result)

    # # Rectangles
    def test_rectangle(self):
        """ test for geometry.rectangle """
        self.assertRaises(ValueError, BaseGeometry.rectangle, "a", 1, 1, 1)
        self.assertRaises(ValueError, BaseGeometry.rectangle, 1, "a", 1, 1)
        self.assertRaises(ValueError, BaseGeometry.rectangle, 1, 1, "a", 1)
        self.assertRaises(ValueError, BaseGeometry.rectangle, 1, 1, 1, "a")

        self.assertEqual(BaseGeometry.rectangle(0, 0, 0, 0), [(0, 0)])
        self.assertCountEqual(BaseGeometry.rectangle(0, 0, 1, 1), [(0, 0), (0, 1), (1, 1), (1, 0)])
        self.assertCountEqual(BaseGeometry.rectangle(1, 1, 0, 0), [(0, 0), (0, 1), (1, 1), (1, 0)])
        self.assertCountEqual(BaseGeometry.rectangle(4, 3, 7, 5), [(4, 3), (4, 4), (4, 5), (5, 5), (6, 5), (7, 5), (7, 4), (7, 3), (6, 3), (5, 3), (6, 4), (5, 4)])
        self.assertCountEqual(BaseGeometry.rectangle(3, 3, 9, 9), [(3, 3), (9, 9), (9, 8), (9, 7), (9, 5), (9, 6), (9, 4), (9, 3), (8, 4), (7, 3), (6, 4), (4, 4),
                                                                   (3, 4), (3, 5), (3, 6), (3, 7), (3, 8), (3, 9), (4, 9), (5, 9), (6, 9), (7, 9), (8, 9), (4, 5),
                                                                   (5, 4), (6, 5), (7, 4), (8, 5), (4, 6), (5, 5), (6, 6), (7, 5), (8, 6), (4, 7), (5, 6), (6, 7),
                                                                   (7, 6), (8, 7), (4, 8), (5, 7), (6, 8), (7, 7), (8, 8), (7, 8), (5, 8), (8, 3), (6, 3), (4, 3),
                                                                   (5, 3)])

    def test_hollow_rectangle(self):
        """ test for geometry.hollow_rectangle """
        self.assertRaises(ValueError, BaseGeometry.hollow_rectangle, "a", 1, 1, 1)
        self.assertRaises(ValueError, BaseGeometry.hollow_rectangle, 1, "a", 1, 1)
        self.assertRaises(ValueError, BaseGeometry.hollow_rectangle, 1, 1, "a", 1)
        self.assertRaises(ValueError, BaseGeometry.hollow_rectangle, 1, 1, 1, "a")

        self.assertEqual(BaseGeometry.hollow_rectangle(0, 0, 0, 0), [(0, 0)])
        self.assertCountEqual(BaseGeometry.hollow_rectangle(0, 0, 1, 1), [(0, 0), (0, 1), (1, 1), (1, 0)])
        self.assertCountEqual(BaseGeometry.hollow_rectangle(1, 1, 0, 0), [(0, 0), (0, 1), (1, 1), (1, 0)])
        self.assertCountEqual(BaseGeometry.hollow_rectangle(4, 3, 7, 5), [(4, 3), (4, 4), (4, 5), (5, 5), (6, 5), (7, 5), (7, 4), (7, 3), (6, 3), (5, 3)])
        self.assertCountEqual(BaseGeometry.hollow_rectangle(3, 3, 9, 9), [(3, 3), (9, 9), (9, 8), (9, 7), (9, 5), (9, 6), (9, 4), (9, 3), (7, 3), (3, 4),
                                                              (3, 5), (3, 6), (3, 7), (3, 8), (3, 9), (4, 9), (5, 9), (6, 9), (7, 9), (8, 9),
                                                              (8, 3), (6, 3), (4, 3), (5, 3)])

    # # Triangles
    def test_triangle(self):
        """ test for geometry.triangle """
        for geometry in (SquareGeometry, FHexGeometry):
            self.assertRaises(ValueError, geometry.triangle, "a", 1, 1, 1, 1)
            self.assertRaises(ValueError, geometry.triangle, 1, "a", 1, 1, 1)
            self.assertRaises(ValueError, geometry.triangle, 1, 1, "a", 1, 1)
            self.assertRaises(ValueError, geometry.triangle, 1, 1, 1, "a", 1)
            self.assertRaises(ValueError, geometry.triangle, 1, 1, 1, 1, -1)

            for i in geometry.ANGLES:
                self.assertCountEqual(geometry.triangle(0, 0, 0, 0, i), [(0, 0)])

    def test_triangle3d(self):
        """ test for geometry.triangle3d """
        for geometry in (SquareGeometry, FHexGeometry):
            self.assertRaises(ValueError, geometry.triangle3d, "a", 1, 1, 1, 1, 1, 1)
            self.assertRaises(ValueError, geometry.triangle3d, 1, "a", 1, 1, 1, 1, 1)
            self.assertRaises(ValueError, geometry.triangle3d, 1, 1, "a", 1, 1, 1, 1)
            self.assertRaises(ValueError, geometry.triangle3d, 1, 1, 1, "a", 1, 1, 1)
            self.assertRaises(ValueError, geometry.triangle3d, 1, 1, 1, 1, "a", 1, 1)
            self.assertRaises(ValueError, geometry.triangle3d, 1, 1, 1, 1, 1, "a", 1)
            self.assertRaises(ValueError, geometry.triangle3d, 1, 1, 1, 1, 1, 1, -1)

        # ## flat hex
        # left to right
        self.assertCountEqual(FHexGeometry.triangle(2, 3, 4, 3, 1), [(3, 3), (3, 4), (3, 3), (4, 5), (4, 4), (4, 3), (4, 2), (4, 1), (4, 1), (3, 1), (3, 2), (2, 3)])
        self.assertCountEqual(FHexGeometry.triangle(2, 3, 4, 3, 2), [(3, 3), (4, 4), (4, 3), (4, 2), (4, 2), (3, 2), (2, 3)])
        self.assertCountEqual(FHexGeometry.triangle(2, 3, 4, 3, 3), [(3, 3), (4, 4), (4, 3), (4, 2), (4, 2), (3, 2), (2, 3)])

        # right to left
        self.assertCountEqual(FHexGeometry.triangle(4, 3, 2, 3, 1), [(3, 2), (3, 1), (3, 2), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 5), (3, 4), (3, 3), (4, 3)])
        self.assertCountEqual(FHexGeometry.triangle(4, 3, 2, 3, 2), [(3, 2), (2, 2), (2, 3), (2, 4), (2, 4), (3, 3), (4, 3)])
        self.assertCountEqual(FHexGeometry.triangle(4, 3, 2, 3, 3), [(3, 2), (2, 2), (2, 3), (2, 4), (2, 4), (3, 3), (4, 3)])

    # # Translations, rotations
    def test_rotate(self):
        """ test for geometry.rotate """
        for geometry in (SquareGeometry, FHexGeometry):
            self.assertRaises(ValueError, geometry.rotate, 0, (0, 0), [(0, 0)], 1)
            self.assertRaises(ValueError, geometry.rotate, 0, "a", [(0, 0)], 1)
            self.assertRaises(ValueError, geometry.rotate, 0, ("a", 0), [(0, 0)], 1)
            self.assertRaises(ValueError, geometry.rotate, 0, (0, 0), 0, 1)
            self.assertRaises(ValueError, geometry.rotate, 0, (0, 0), ["a", (0, 0)], 1)
            self.assertRaises(ValueError, geometry.rotate, 0, (0, 0), [("a", 0), (0, 0)], 1)
            self.assertRaises(ValueError, geometry.rotate, 0, (0, 0), 1, "a")

        # ## Flat hex
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
            self.assertCountEqual(FHexGeometry.rotate((6, 6), [(6, 6)], i), [(6, 6)])
            result = FHexGeometry.rotate((6, 6), [(5, 5), (4, 5), (6, 6)], i)
            self.assertCountEqual(result, attended[i])

        # ## Square
        attended = [
                    [(6, 6), (6, 5), (5, 5), (5, 6)],
                    [(6, 6), (5, 6), (5, 7), (6, 7)],
                    [(6, 6), (6, 7), (7, 7), (7, 6)],
                    [(6, 6), (7, 6), (7, 5), (6, 5)],
                    [(6, 6), (6, 5), (5, 5), (5, 6)]
                   ]

        for i in range(len(attended)):
            self.assertCountEqual(SquareGeometry.rotate((6, 6), [(6, 6)], i), [(6, 6)])
            result = SquareGeometry.rotate((6, 6), [(6, 6), (6, 5), (5, 5), (5, 6)], i)
            self.assertCountEqual(result, attended[i])

if __name__ == "__main__":
    unittest.main()
