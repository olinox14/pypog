'''
    Profiling performance of the geometry functions
'''

import cProfile
import timeit

from pypog import geometry

_profile = ['geometry.squ2_line(0,0,1000,1000)',
            'geometry.fhex2_line(0,0,1000,1000)',
            'geometry.rectangle(0,0,1000,1000)',
            'geometry.hollow_rectangle(0,0,1000,1000)',
            'geometry.squ2_triangle(0,0,100,100,2)',
            'geometry.fhex2_triangle(0,0,100,100,2)',
#             'geometry.squ3_triangle(0,0,0,100,100,100,2)',
#             'geometry.fhex3_triangle(0,0,0,100,100,100,2)',
            'geometry.fhex2_pivot((0,0),[(i, j) for i in range(1, 100) for j in range(1,100)], 1)',
            'geometry.squ2_pivot((0,0),[(i, j) for i in range(1, 100) for j in range(1,100)], 1)',
            ]

for _call in _profile:
    print(">> {}".format(_call))
    cProfile.run(_call, sort='nfl')

    number = 1
    t = 0
    while 1:
        t = timeit.timeit(lambda: eval(_call), number=number)
        if t >= 1:
            break
        elif number > 1000000:
            print("error: number superior to a million")
            number = "err"
            t = "?"
            break
        number *= 10

    print("Timeit (x{}): {} s.\n".format(number, t))
    print("".join(["-" for _ in range(30)]))


