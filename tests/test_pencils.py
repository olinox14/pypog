'''

    ** By Cro-Ki l@b, 2017 **
'''
import unittest

from pypog.grid_objects import SquareGrid, FHexGrid
from pypog.painter_objects import BasePainter, NotStartedException


class Test(unittest.TestCase):

    def test_base_painter(self):
        for grid_cls in (SquareGrid, FHexGrid):

            self.assertRaises(TypeError, BasePainter, "invalid arg")

            grid = grid_cls(30, 30)
            painter = BasePainter(grid)

            # default origin and position
            self.assertEqual(painter.origin, None)
            self.assertEqual(painter.position, None)

            with self.assertRaises(AttributeError):
                painter.origin = (1, 1)
                painter.position = (1, 1)

            # size
            self.assertRaises(TypeError, setattr, painter, "size", "a")
            self.assertRaises(ValueError, setattr, painter, "size", -1)
            self.assertEqual(painter.size, 1)

            # selection, added, removed
            self.assertEqual(painter.selection, [])
            self.assertEqual(painter.added, [])
            self.assertEqual(painter.removed, [])

            # painter methods
            self.assertRaises(TypeError, painter.start, "a")
            self.assertRaises(NotStartedException, painter.update, 1, 1)
            self.assertRaises(NotImplementedError, painter._update)

            try:
                painter.start(0, 0)
            except NotImplementedError:
                pass
            self.assertRaises(TypeError, painter.update, "a")
            self.assertEqual(painter.origin, (0, 0))

    def test_line_painter(self):
        pass

    def test_free_painter(self):
        pass

    def test_pot_painter(self):
        pass

    def test_rect_painter(self):
        pass

    def test_hrect_painter(self):
        pass

    def test_boundary_painter(self):
        pass



if __name__ == "__main__":
    unittest.main()
