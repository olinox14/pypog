'''
    Painter classes allow you to get an evolving selection of coordinates, according to the type of painter you use.

    Start it, set size (default: 1), update it as many times you want with new positions on the grid, then
    get the list of selected coordinates, or the list of added / removed coorinates by the last update.

    Connect those functions to your graphical grid, and let it do the job.

    Example of use:
        On mouse left button down on a (x, y) cell: painter.start(x, y)
        On hover event on cells: painter.update(), then display the result on your grid
        On mouse left button up: Apply the modification on your grid, then delete your painter object

    ** By Cro-Ki l@b, 2017 **
'''
from pypog import grid_objects
from pypog.geometry_objects import BaseGeometry


class NotStartedException(Exception):
    pass

class AlreadyStartedException(Exception):
    pass

class BasePainter(object):
    """ Base class for painters """
    def __init__(self, grid):
        # do we really need the grid ref? cell_shape could be enough?
        if not isinstance(grid, grid_objects.BaseGrid):
            raise TypeError("'grid' should be a Grid object (given: {})".format(grid))
        self._grid = grid

        self._origin = None
        self._position = None

        self._size = 1
        self._previous = set()
        self._selection = set()

    @property
    def origin(self):
        """returns the coordinates of the cell where the painting began
        This property is read-only: use the 'start' method to set it"""
        return self._origin

    @property
    def size(self):
        """returns the current size of the painter"""
        return self._size

    @size.setter
    def size(self, size):
        """sets the current size of the painter
        size has to be a strictly positive integer"""
        if not isinstance(size, int):
            raise TypeError("size has to be an integer (given: {})".format(size))
        if not size > 0:
            raise ValueError("size has to be strictly positive (given: {})".format(size))
        self._size = size

    @property
    def position(self):
        """returns the current (x, y) position of the painter
        This property is read-only: use the 'update' method to give it a new value"""
        return self._position

    @property
    def selection(self):
        """return the current list of coordinates selected by the painter (read-only)"""
        return list(self._selection)

    @selection.setter
    def selection(self, new_selection):
        self._previous = self._selection
        self._selection = new_selection

    @property
    def added(self):
        """return the list of coordinates added to the last selection by the last update """
        return list(self._selection - self._previous)

    @property
    def removed(self):
        """return the list of coordinates removed from the last selection by the last update """
        return list(self._previous - self._selection)

    def start(self, x0, y0):
        """start a new painting
        (x0, y0) is the origin of the painting, and will not be modified."""
        if self._selection:
            raise AlreadyStartedException("the painter has already been started")
        self._origin = (x0, y0)
        self.update(x0, y0)

    def update(self, x, y):
        """Updates the current position of the painter
        If (x, y) is not in the position's history, it updates the current selection, and the added / removed lists."""
        BaseGeometry.assertCoordinates((x, y))
        if self._origin == None:
            raise NotStartedException("Painter has to be started before any update: use 'start' method")
        self._position = (x, y)
        self._update()

    def _update(self):
        """this method update the selection, added and removed lists,
        depending on the current size, position, origin
        Override it to create your own painter"""
        # this method should be overrided to update the 'self._selection' attribute
        raise NotImplementedError("_update method has to be overrided")

class LinePainter(BasePainter):
    """Paint a 2d line between origin and position"""
    def __init__(self, *args):
        BasePainter.__init__(self, *args)

    def _update(self):
        line = set(self._grid.line(*self._origin, *self._position))
        result = line
        if self._grid.size > 1:
            for x, y in line:
                result |= set(self._grid.zone(x, y, self.size - 1))
        self.selection = result

class FreePainter(BasePainter):
    """Free handed painter"""
    def __init__(self, *args):
        BasePainter.__init__(self, *args)

    @property
    def removed(self):
        return []  # there can't be any removed coordinates with this painter

    def _update(self):
        self.selection |= set(self._grid.zone(*self.position, self.size))

class PaintPotPainter(BasePainter):
    """ This particular painter selects all cells of same nature from nearest to nearest

    The 'same nature' is confirmed by passing a comparaison method to the painter
    This method should take x1, y1, x2, y2 as args, and return a boolean: True for similar cells, False in other case

    WARNING: this painter result is not affected by the 'update' method,
    because the result is already known at starts

    usage:

        # your comparison function
        my_grid = HexGrid(30,30)

        def identical_cells_function(x1, y1, x2, y2):
            return my_grid[(x1, y1)] == my_grid[(x2, y2)].color:

        my_painter = PaintPotPainter(my_grid)
        my_painter.start(3, 3, identical_cells_function)

        print(my_painter.selection)

    """

    def __init__(self, *args):
        BasePainter.__init__(self, *args)
        self._comp_pointer = (lambda x: False)

    def start(self, x0, y0):
        BasePainter.start(self, x0, y0)

    def update(self, *args):
        if not self.selection:
            BasePainter.update(self, *args)

    @property
    def removed(self):
        return []

    @property
    def added(self):
        return self.selection

    def _update(self):
        current_selection = { self._origin }

        buffer = set(self._grid.neighbours(*self._origin))
        while buffer:
            pos = buffer.pop()
            if self._grid._compare_cells(*self._origin, *pos):
                current_selection.add(pos)
                buffer |= (set(self._grid.neighbours(*pos)) - current_selection)

        self.selection = current_selection

class RectanglePainter(BasePainter):
    """ RectanglePainter draw a plain rectangle with origin being the
    top left corner, and position the bottom right corner"""
    def __init__(self, *args):
        BasePainter.__init__(self, *args)

    def _update(self):
        self.selection = set(self._grid.rectangle(*self._origin, *self._position))

class HollowRectanglePainter(BasePainter):
    """ HollowRectanglePainter draw an hollow rectangle with origin being the
    top left corner, and position the bottom right corner"""
    def __init__(self, *args):
        BasePainter.__init__(self, *args)

    def _update(self):
        self._selection = set(self._grid.hollow_rectangle(*self._origin, *self._position))

class BoundaryPainter(BasePainter):
    """ BoundaryPainter is a particular painter which select all the cells
    on the left of a straight line which could be oriented
    from 0, 45, 90, 135, 180, 225, 270, 315 degrees
    Orientation  of the boudary depends on position and origin."""
    def __init__(self, *args):
        BasePainter.__init__(self, *args)

    def _update(self):

        x0, y0 = self._origin
        x, y = self._position
        dx, dy = x - x0, y - y0

        if dx == 0:  # vertical boudary
            self.selection = {(x, y) for x, y in self._grid if (x - x0) * dy >= 0}

        elif dy == 0:  # horizontal boundary
            self.selection = {(x, y) for x, y in self._grid if (y - y0) * (-dx) >= 0}

        elif dx > 0 and dy < 0:  # normal vector to the top left
            self.selection = {(x , y) for x, y in self._grid if (x - x0) + (y - y0) <= 0}

        elif dx > 0 and dy > 0:  # normal vector to the top right
            self.selection = {(x , y) for x, y in self._grid if (x - x0) - (y - y0) >= 0}

        elif dx < 0 and dy < 0:  # normal vector to bottom left
            self.selection = {(x , y) for x, y in self._grid if -(x - x0) + (y - y0) >= 0}

        elif dx < 0 and dy > 0:  # normal vector to bottom right
            self.selection = {(x , y) for x, y in self._grid if -(x - x0) - (y - y0) <= 0}

        else:  # origin equal position
            self.selection = set()
