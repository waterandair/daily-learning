#!/usr/bin/python
# -*- coding utf-8 -*-

"""
If you want to implement a new kind of iteration pattern, define it using a generator function.
Here's a generator that produces a range of floating-point numbers
"""
def frange(start, stop, increment):
    x = start
    while x < stop:
        yield x
        x += increment


for n in frange(0, 5, 0.5):
    print(n)

"""
0
0.5
1.0
1.5
2.0
2.5
3.0
3.5
4.0
4.5
"""

print(list(frange(0, 1, 0.125)))  # [0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875]