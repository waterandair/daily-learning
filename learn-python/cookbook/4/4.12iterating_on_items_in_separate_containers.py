#!/usr/bin/python
# -*- coding utf-8 -*-
from itertools import chain

"""
You need to perform the same operation on many objects, but the objects are contained in different containers,and you'd
like to avoid nested loops without losing the readability of your code
"""

a = [1, 2, 3, 4]
b = ['x', 'y', 'z']
for x in chain(a, b):
    print(x)

"""
1
2
3_num_date_time
4
x
y
z
"""


active_items = set()
inactive_items = set()

for item in chain(active_items, inactive_items):
    pass


# Inefficent
# for x in a + b:
#     ...
#
# Better
# for x in chain(a, b):
#     ...