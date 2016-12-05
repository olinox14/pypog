# pypog - Python Play on Grid

Generates an hexagonal or square grid and implement it in your game!

*pypog is under [GNU License](https://github.com/olinox14/pypog/blob/master/LICENSE.txt)*

[![Build Status](https://travis-ci.org/olinox14/pypog.svg?branch=master)](https://travis-ci.org/olinox14/pypog) [![Coverage Status](https://coveralls.io/repos/github/olinox14/pypog/badge.svg?branch=master)](https://coveralls.io/github/olinox14/pypog?branch=master)

### Pypog is currently on developpement, do not hesitate to involve!



### pypog gives you access to many tools to play with grids:

* Square or hexagonal grids
* Geometrical functions: lines, zones, rectangles, cones
* Each of them come in 2D or 3D version
* Pencils: freehand, line, zone, rectangles, zone, boundaries
* Pathfinding (based on A* algorythm)
* 3D space occupation

### Examples of use
	
	grid = HexGrid(50,50)
	print(grid.line(3,3,30,30))
	
	>> [(3, 3), (4, 4), (4, 5), (5, 5), (6, 6), (6, 7), (7, 7), (8, 8), (9, 8), (9, 9), (10, 10)]

	grid = HexGrid(50,50)
	print(grid.zone(3,3,2))

	>> [(3, 2), (1, 3), (5, 4), (4, 5), (1, 4), (2, 3), (4, 2), (2, 5), (5, 3), (1, 2), (3, 5), (3, 3), (4, 4), (3, 1), (4, 3), (2, 2), (3, 4), (2, 4), (5, 2)]
	
	grid = HexGrid(50,50)
	print(grid.rect(3,3,6,6))

	>> [(3, 3), (3, 4), (3, 5), (3, 6), (4, 3), (4, 4), (4, 5), (4, 6), (5, 3), (5, 4), (5, 5), (5, 6), (6, 3), (6, 4), (6, 5), (6, 6)]

	grid = HexGrid(50,50)
	print(grid.hollow_rect(3,3,6,6))

	>> [(3, 3), (3, 4), (3, 5), (3, 6), (4, 3), (4, 6), (5, 3), (5, 6), (6, 3), (6, 4), (6, 5), (6, 6)]


### Override pypog classes

Override pypog Grid or Cell classes to build your own game.

### Credits:

Many thanks to:

* [redblobgames.com](http://www.redblobgames.com/grids/hexagons/)
* [roguebasin.com](http://www.roguebasin.com/index.php?title=Bresenham%27s_Line_Algorithm)
* [policyalmanac.org](http://www.policyalmanac.org/games/aStarTutorial.htm)