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
from pypog.grid_objects import BaseGrid

class NoPathFound(Exception):
    pass

class Node():
    target = None
    def __init__(self, x, y, parent=None):
        self._x = x
        self._y = y
        self.parent = parent
        self.gcost = 0
        self.hcost = 0

    def compute(self, moving_cost):
        # the manhattan distance to the final target
        self.hcost = HexGeometry.cubic_distance(self._x, self._y, *self.target)

        # the cumulated moving cost of the path that lead here
        self.gcost = self.parent.g_cost + self.moving_cost

    @property
    def cost(self):
        return self.g_cost + self.h_cost

def path(grid, from_x, from_y, to_x, to_y):
    """return the shorter path from origin to target on the Grid object
    the path is estimated following:
    - geometry of the grid
    - altitudes of the cells
    - cost of the move returned by the 'moving_cost_function'

    origin and target should be Cell objects
    """
    if not isinstance(grid, BaseGrid):
        raise TypeError("grid has to be an instance of BaseGrid (given: {})".format(type(grid).__name__))

    nodes = {}

    # pass target to the Node class:
    Node.target = (to_x, to_y)

    # origin node
    nO = Node(from_x, from_y)

    # current position
    pos = nO

    while (pos.x, pos.y) != (to_x, to_y):

        # lists the neighbors of the current position
        neighbours = grid.neighbors(pos.x, pos.y)



        # removes the coordinates already checked
        neighbours = set(neighbours) - set(nodes.keys())

        for x, y in neighbours:

            # use the grid's movingcost() function to get the moving cost from position to (x, y)
            cost = grid._movingcost(pos.x, pos.y, x, y)

            # cost is negative, can not go there
            if cost < 0:
                continue

            # instanciate the new node with 'pos' as parent
            node = Node(x, y, pos)
            node.compute(cost)

            # check if there is already a node with a lower cost
            try:
                if nodes[(x, y)].cost <= node.cost:
                    continue
            except KeyError:
                pass

            # memorize the node
            nodes[(x, y)] = node

        # no new nodes were found
        if not nodes:
            raise NoPathFound()

        # retrieves the lowest cost
        best = min(nodes.values(), key=lambda x: x.cost)

        del nodes[best.coord]
        pos = best

    else:

        # build the result
        path = []
        while (pos.x, pos.y) != (from_x, from_y):
            path.insert(0, (pos.x, pos.y, pos.k_dep))
            pos = pos.parent

    return path
