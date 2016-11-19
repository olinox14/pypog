'''
Created on 17 déc. 2015
   Implement the A* algorithm
@author: olivier.massot
'''
from core.geometry import cube_coords


def distance(coord1, coord2):
    """distance between 1 and 2"""
    x1, y1 = coord1
    xu1, yu1, zu1 = cube_coords.cv_off_cube(x1, y1)
    x2, y2 = coord2
    xu2, yu2, zu2 = cube_coords.cv_off_cube(x2, y2)
    return max(abs(xu1 - xu2), abs(yu1 - yu2), abs(zu1 - zu2))

def square_distance(coord1, coord2):
    """distance between 1 and 2 (quicker than distance)"""
    return (coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2

class Path(object):
    def __init__(self):
        self._cells = []
        self._costs = []
        self._modes = []
        self._val = []

class Node():
    def __init__(self, coord):
        self.parent = None    # coords of the previous node
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
        self.cout =  self.g_cost + self.h_cost
    
    def parent(self):
        return self.parent
    
    def distance(self, coord1, coord2):
        """distance (en cases) entre deux coordonnees"""
        x1, y1 = coord1
        x2, y2 = coord2
        return cube_coords.distance_off(x1, y1, x2, y2)
    

def path(grid, origin, target, abilities = None):
    """return the shorter path from origin to target on the Grid object
    the path is estimated following:
    - geometry of the grid
    - altitudes of the cells
    - land use of the cells
    - type of moves allowed on the cells
    - moving abilities
    
    origin and target should be Cell objects
    """
    nodes = {}  # coord: node

    nO = Node(origin)
    nO.parent = None
    nO.cost = 0

#     kept = [nO]
    path = []
    position = nO
    
    while position.coord != target:

        # we could avoid the re-computing
        neighbours = grid.cell(position.coord).neighbours
        
        for coord in [coord for coord in neighbours if not coord in nodes.keys()]:

                # !!! need a calculate cost function !!!
                cost = 1
                if cost < 0:
                    continue
                
                node = Node(coord)
                
                node.create(position, target, cost)

                try:
                    existing = nodes[coord]
                    if existing.cout <= node.cout:
                        continue
                except KeyError:
                    pass
                
                nodes[coord] = node

        if len(nodes) == 0:
            print("No path found")
            return []
        
        best = min(nodes.values(), key=lambda x: x.cout)
#         retenus.append(meilleur)
        del nodes[best.coord]
        position = best
    
    else:
        # build the result
        while position.coord != origin:
            path.insert(0, (position.coord, position.k_dep))
            position = position.parent
    
    return path   
