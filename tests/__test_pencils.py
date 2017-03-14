'''

    ** By Cro-Ki l@b, 2017 **
'''
import unittest

from pypog import geometry, grid_objects, painting

class Test(unittest.TestCase):

    def test_base_pencil(self):
        for cell_shape in (geometry.FLAT_HEX, geometry.SQUARE):

            self.assertRaises(TypeError, painting.BasePencil, "invalid arg")

            grid = grid_objects.Grid(cell_shape, 30, 30)
            my_pencil = painting.BasePencil(grid)

            # default origin and position
            self.assertEqual(my_pencil.origin, None)
            self.assertEqual(my_pencil.position, None)
            self.assertRaises(AttributeError, my_pencil.origin, (1, 1))
            self.assertRaises(AttributeError, my_pencil.position, (1, 1))

            # size
            self.assertRaises(TypeError, setattr, my_pencil, "size", "a")
            self.assertRaises(ValueError, setattr, my_pencil, "size", -1)
            self.assertEqual(my_pencil.size, 1)

            # selection, added, removed
            self.assertEqual(my_pencil.selection, [])
            self.assertEqual(my_pencil.added, [])
            self.assertEqual(my_pencil.removed, [])

            # pencil methods
            self.assertRaises(TypeError, my_pencil.start, "a")
            self.assertRaises(painting.NotStartedException, my_pencil.update, 1, 1)
            self.assertRaises(NotImplementedError, my_pencil._update)

            try:
                my_pencil.start(0, 0)
            except NotImplementedError:
                pass
            self.assertRaises(TypeError, my_pencil.update, "a")
            self.assertEqual(my_pencil.origin, (0, 0))

    def test_line_pencil(self):
        pass

    def test_free_pencil(self):
        pass

    def test_pot_pencil(self):
        pass

    def test_rect_pencil(self):
        pass

    def test_hrect_pencil(self):
        pass

    def test_boundary_pencil(self):
        pass



if __name__ == "__main__":
    unittest.main()
