'''
   Implements the A* algorithm

   usage:

       grid = SquareGrid(30, 30)
       p = Pathfinder.a_star(grid, (1, 6), (3, 9))
       >> [(2, 7), (3, 8), (3, 9), (3, 9)]

    * 'grid': Grid object
    * 'origin' starting (x, y) coordinates
    * 'target' targeted (x, y) coordinates

    ** By Cro-Ki l@b, 2017 **
'''
import heapq

from pypog.geometry_objects import BaseGeometry


class NoPathFound(Exception):
    pass

class Node(tuple):
    def __new__(self, x, y, parent=None):
        n = tuple.__new__(self, (x, y))
        n.parent = parent
        n.cost = 0
        return n

class NodesHeap():
    def __init__(self):
        self._lst = []

    def push(self, node, priority):
        heapq.heappush(self._lst, (priority, node))

    def pop(self):
        return heapq.heappop(self._lst)[1]


class Pathfinder():

    @staticmethod
    def a_star(grid, origin, target):

        BaseGeometry.assertCoordinates(origin, target)

        # list of checked nodes
        nodes = NodesHeap()

        # starting node, cost is 0 and parent is None
        origin = Node(*origin)

        # append 'origin' to nodes, with priority 0
        nodes.push(origin, 0)

        # while there remains unchecked nodes , process
        while nodes:

            # pop the node with the lowest priority (cost) from the list,
            current = nodes.pop()

            # early exit
            if current == target:
                break

            for x, y in grid.neighbors(*current):

                node = Node(x, y, current)

                # get the moving cost to this node
                movingcost = grid.movingcost(*current, *node)
                if movingcost < 0:
                    continue

                # cost of the node is the accumulated cost from origin
                node.cost = current.cost + movingcost

                # priority of the node is the sum of its cost and distance to target
                # (the lower the better)
                priority = node.cost + grid.geometry.manhattan(*node, *target)

                # (?) would it be necessary to check if there is already a
                # node with same coordinates and a lower priority?

                # append to the checked nodes list
                nodes.push(node, priority)
        else:
            # all the reachable nodes hve been checked, no way found to the target
            raise NoPathFound("no path were found to the targetted location {}".format(target))

        # build the result by going back up from target to origin
        result = [target]
        while current != origin:
            result.append(tuple(current))
            current = current.parent
        result.append(origin)
        result.reverse()

        return result

if __name__ == '__main__':
    from pypog.grid_objects import SquareGrid
    grid = SquareGrid(30, 30)
    p = Pathfinder.a_star(grid, (1, 6), (3, 9))
    print(p)

