'''
   Implement the A* algorithm

   Use the path function like that:

       path(my_grid, (xs, ys), (xt, yt), my_moving_cost_function)
       >> [(xs, ys), (x1, y1), (x2, y2), ...(xt, yt)]

       where:
        - my_grid is a Grid, HexGrid, or SquareGrid object
        - (xs, ys) is the starting cell
        - (xt, yt) is the targeted cell
        - my_moving_cost_function is a pointer to your custom function. This function should be like:

        def my_moving_cost_function((x0, y0), (x1, y1)):
            ...
            return cost

        this function should return an INTEGER which represent the cost of a move from (x0, y0) to (x1, y1),
        where (x0, y0) and (x1, y1) are adjacent cells

        If cost is negative, move is impossible.
        If move is strictly positive, it represents the difficulty to move from 0 to 1:
        the returned path will be the easiest from (xs, ys) to (xt, yt)

    3D paths:
        The path method takes account of the differents altitudes of the cells, but it is not designed to
        work for a flying mover.
        More clearly: the path will be on the ground: walking, climbing, but no flying for instance.

    ** By Cro-Ki l@b, 2017 **
'''
from pypog.geometry_objects import HexGeometry

def distance(coord1, coord2):
    """distance between 1 and 2"""
    x1, y1 = coord1
    xu1, yu1, zu1 = HexGeometry.cv_off_cube(x1, y1)
    x2, y2 = coord2
    xu2, yu2, zu2 = HexGeometry.cv_off_cube(x2, y2)
    return max(abs(xu1 - xu2), abs(yu1 - yu2), abs(zu1 - zu2))

def square_distance(coord1, coord2):
    """distance between 1 and 2 (quicker than distance)"""
    return (coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2

class Path(object):
    def __init__(self):
        self._cells = []
        self._costs = []
        self._modes = []
        self._val = []

class Node():
    def __init__(self, coord):
        self.parent = None  # coords of the previous node
        self.coord = coord
        self.k_dep = 1
        self.g_cost = 0
        self.h_cost = 0
        self.cost = 0

    def create(self, parent, target, k_dep):
        self.parent = parent
        self.k_dep = k_dep
        self.h_cost = self.distance(self.coord, target)
        self.g_cost = self.parent.g_cost + self.k_dep
        self.cout = self.g_cost + self.h_cost

    def parent(self):
        return self.parent

    def distance(self, coord1, coord2):
        """distance (en cases) entre deux coordonnees"""
        x1, y1 = coord1
        x2, y2 = coord2
        return HexGeometry.distance_off(x1, y1, x2, y2)

def _default_moving_cost_function(from_coord, to_coord):
    return 1

def path(grid, origin, target, moving_cost_function=None):
    """return the shorter path from origin to target on the Grid object
    the path is estimated following:
    - geometry of the grid
    - altitudes of the cells
    - cost of the move returned by the 'moving_cost_function'

    origin and target should be Cell objects
    """
    if moving_cost_function == None:
        moving_cost_function = _default_moving_cost_function

    nodes = {}  # coord: node

    nO = Node(origin)
    nO.parent = None
    nO.cost = 0

#     kept = [nO]
    path = []
    position = nO

    while position.coord != target:

        # we maybe could avoid the re-computing by storing the neighbours coordinates?
        neighbours = grid.cell(position.coord).neighbours

        for coord in [coord for coord in neighbours if not coord in nodes.keys()]:

                cost = moving_cost_function(position.coord, coord)
                if cost < 0:
                    continue

                node = Node(coord)

                node.create(position, target, cost)

                try:
                    existing = nodes[coord]
                    if existing.cost <= node.cost:
                        continue
                except KeyError:
                    pass

                nodes[coord] = node

        if len(nodes) == 0:
            print("No path found")
            return []

        best = min(nodes.values(), key=lambda x: x.cost)
        del nodes[best.coord]
        position = best

    else:
        # build the result
        while position.coord != origin:
            path.insert(0, (position.coord, position.k_dep))
            position = position.parent

    return path
