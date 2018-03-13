#!/usr/bin/python3
# -*- coding utf-8 -*-
from itertools import zip_longest

"""
You want to iterate over the items contained in more than one sequence at a time
"""

"""
To iterate over more than one sequence simultaneously, use the zip() function
"""


xpts = [1, 5, 4, 2, 10, 7]
ypts = [101, 78, 37, 15, 62, 99]
for x, y in zip(xpts, ypts):
    print(x, y)

"""
1 101
5 78
4 37
2 15
10 62
7 99
"""


"""
The length of the iteration is the same as the length of the shortest input
"""
a = [1, 2, 3]
b = ['w', 'x', 'y', 'z']

for i in zip(a, b):
    print(i)

"""
(1, 'w')
(2, 'x')
(3, 'y')
"""

"""
If this behavior is not desired, use itertools.zip_longest() instead
"""

for i in zip_longest(a, b):
    print(i)
"""
(1, 'w')
(2, 'x')
(3, 'y')
(None, 'z')
"""
