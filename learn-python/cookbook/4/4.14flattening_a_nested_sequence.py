#!/usr/bin/python3
# -*- coding utf-8 -*-
from collections import Iterable

"""
You have a nested sequence that you want to flatten into a single list of values.
This is easily solved by writing a recursive generator function involving a yield from statement
"""


def flatten(items, ignore_types=(str, bytes)):
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, ignore_types):
            yield from flatten(x)
        else:
            yield x


items = [1, 2, [3, 4, [5, 6], 7], 8]

for x in flatten(items):
    print(x)


"""
1
2
3_num_date_time
4
5
6
7
8
"""

"""!!!
It should be noted that 
"""