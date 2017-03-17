'''
   Implements the A* algorithm

   usage:
       grid = SquareGrid(30, 30)
       p = path(grid, (1, 6), (3, 9))
       >> [(2, 7), (3, 8), (3, 9), (3, 9)]

    * 'grid': Grid object
    * 'origin' starting (x, y) coordinates
    * 'target' targeted (x, y) coordinates

    ** By Cro-Ki l@b, 2017 **
'''
import heapq

class NoPathFound(Exception):
    pass

class Node(tuple):
    def __new__(self, x, y, parent=None):
        n = tuple.__new__(self, (x, y))
        n.parent = parent
        n.cost = 0
        return n

def path(grid, origin, target, include_origin):

    # list of checked nodes
    nodes = []

    # starting node, cost is 0 and parent is None
    origin = Node(*origin)

    # append 'origin' to nodes, with priority 0
    heapq.heappush(nodes, (0, origin))

    # while there are unchecked nodes , process
    while nodes:

        # pop the node with the lowest priority (cost) from the list,
        current = heapq.heappop(nodes)[1]

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

            # check if there is already a node with a lower cost
            try:
                index = nodes.index(node)
                if nodes[index].cost > node.cost:
                    del nodes[index]
                else:
                    continue
            except ValueError:
                pass

            # compute the cost of the node
            priority = node.cost + grid.geometry.manhattan(*node, *target)

            # append to the checked nodes list
            heapq.heappush(nodes, (priority, node))
    else:
        # all the reachable nodes hve been checked, no way found to the target
        raise NoPathFound("no path were found to the targetted location {}".format(target))

    # build the result
    result = [target]
    while current != origin:
        result.append(tuple(current))
        current = current.parent
    result.reverse()

    return result

if __name__ == '__main__':
    from pypog.grid_objects import SquareGrid
    grid = SquareGrid(30, 30)
    p = path(grid, (1, 6), (3, 9))
    print(p)

