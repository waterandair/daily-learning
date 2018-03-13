#!/usr/bin/python3
# -*- coding utf-8 -*-
import math
import operator
"""
For simple cases, you might use getattr()
"""
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return 'Point({!r:}, {!r:})'.format(self.x, self.y)

    def distance(self, x, y):
        return math.hypot(self.x - x, self.y -y)


p = Point(2, 3)
d = getattr(p, 'distance')(0, 0)  # 3.605551275463989


"""
An alternative approach is to use operator.methodcaller()
"""
d = operator.methodcaller('distance', 0, 0)(p)
print(d)  # 3.605551275463989


"""
operator.methodcaller() may be useful if you want to look up a method by name and supply the same arguments over
and over again
for instance, if you need to sort an entire list of points
"""
points = [
    Point(1, 2),
    Point(3, 0),
    Point(10, -3),
    Point(-5, -7),
    Point(-1, 8),
    Point(3, 2)
]

# sort by distance from origin (0, 0)
points.sort(key=operator.methodcaller('distance', 0, 0))
print(points)  # [Point(1, 2), Point(3, 0), Point(3, 2), Point(-1, 8), Point(-5, -7), Point(10, -3)]