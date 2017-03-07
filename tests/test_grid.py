'''

    ** By Cro-Ki l@b, 2017 **
'''
import unittest

from pypog.geometry_objects import SquareGeometry, FHexGeometry, BoundingRect
from pypog.grid_objects import BaseGrid, SquareGrid, FHexGrid


class Test(unittest.TestCase):

    def assertObjEquals(self, obj1, obj2):
        self.assertEqual(obj1.__dict__, obj2.__dict__)

    def test_init(self):
        # square grid
        _ = BaseGrid(1, 1)
        _ = SquareGrid(1, 1)
        _ = FHexGrid(1, 1)
        self.assertObjEquals(SquareGrid(1, 1), BaseGrid.from_geometry(SquareGeometry, 1, 1))
        self.assertObjEquals(FHexGrid(1, 1), BaseGrid.from_geometry(FHexGeometry, 1, 1))
        self.assertRaises(TypeError, BaseGrid.from_geometry, int, 1, 1)

    def test_various(self):
        self.assertEqual(str(BaseGrid(1, 1)), "<BaseGrid object>")
        self.assertEqual(str(SquareGrid(1, 1)), "<SquareGrid object>")
        self.assertEqual(str(FHexGrid(1, 1)), "<FHexGrid object>")

    def test_properties(self):
        grid = BaseGrid(1, 1)
        self.assertEqual(grid.height, 1)
        self.assertEqual(grid.width, 1)

        grid.height = 1000
        self.assertEqual(grid.height, 1000)
        grid.width = 1000
        self.assertEqual(grid.width, 1000)

        def _set_invalid_height():
            grid.height = -1
        self.assertRaises(ValueError, _set_invalid_height)

        def _set_invalid_width():
            grid.width = -1
        self.assertRaises(ValueError, _set_invalid_width)

        self.assertEqual(grid.br, BoundingRect(0, 0, 999, 999))

    def test_length(self):
        grid = BaseGrid(1, 1)
        self.assertEqual(len(grid), 1)

        grid.width = 100
        grid.height = 100
        self.assertEqual(len(grid), 10000)

    def test_contains(self):
        grid = BaseGrid(10, 10)
        self.assertTrue((5, 5) in grid)
        self.assertFalse((11, 5) in grid)
        self.assertFalse((5, 11) in grid)
        self.assertFalse("a" in grid)

    def test_iter(self):
        grid = BaseGrid(2, 2)
        self.assertCountEqual([(x, y) for x, y in grid], [(0, 0), (0, 1), (1, 0), (1, 1)])

    def test_geometry(self):
        # geometrics algorithms are properly tested in tests.test_geometry
        square_grid = SquareGrid(10, 10)
        fhex_grid = FHexGrid(10, 10)

        args = (0, 0)
        self.assertEqual(square_grid.neighbors(*args), SquareGeometry.neighbors(*args))
        self.assertEqual(fhex_grid.neighbors(*args), FHexGeometry.neighbors(*args))

        args = (0, 0, 3, 3)
        self.assertEqual(square_grid.line(*args), SquareGeometry.line(*args))
        self.assertEqual(fhex_grid.line(*args), FHexGeometry.line(*args))

        args = (0, 0, 0, 3, 3, 3)
        self.assertEqual(square_grid.line3d(*args), SquareGeometry.line3d(*args))
        self.assertEqual(fhex_grid.line3d(*args), FHexGeometry.line3d(*args))

        args = (0, 0, 1)
        self.assertEqual(square_grid.zone(*args), SquareGeometry.zone(*args))
        self.assertEqual(fhex_grid.zone(*args), FHexGeometry.zone(*args))

        args = (0, 0, 2, 2 , 1)
        self.assertEqual(square_grid.triangle(*args), SquareGeometry.triangle(*args))
        self.assertEqual(fhex_grid.triangle(*args), FHexGeometry.triangle(*args))

        args = (0, 0, 0, 2, 2, 2, 1)
        self.assertEqual(square_grid.triangle3d(*args), SquareGeometry.triangle3d(*args))
        self.assertEqual(fhex_grid.triangle3d(*args), FHexGeometry.triangle3d(*args))

        args = (0, 0, 3, 3)
        self.assertEqual(square_grid.rectangle(*args), SquareGeometry.rectangle(*args))
        self.assertEqual(fhex_grid.rectangle(*args), FHexGeometry.rectangle(*args))

        args = (0, 0, 3, 3)
        self.assertEqual(square_grid.hollow_rectangle(*args), SquareGeometry.hollow_rectangle(*args))
        self.assertEqual(fhex_grid.hollow_rectangle(*args), FHexGeometry.hollow_rectangle(*args))

        args = ((5, 5), [(6, 6)], 1)
        self.assertEqual(square_grid.rotate(*args), SquareGeometry.rotate(*args))
        self.assertEqual(fhex_grid.rotate(*args), FHexGeometry.rotate(*args))

if __name__ == "__main__":
    unittest.main()
