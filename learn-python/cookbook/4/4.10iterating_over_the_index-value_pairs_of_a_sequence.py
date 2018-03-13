#!/usr/bin/python3
# -*- coding utf-8 -*-

my_list = ['a', 'b', 'c']
for idx, val in enumerate(my_list):
    print(idx, val)


"""
0 a
1 b
2 c

in python2.7:
            (0, 'a')
            (1, 'b')
            (2, 'c')
"""

for idx, val in enumerate(my_list, 1):
    print(idx, val)

"""
1 a
2 b
3 c
"""

"""
enumerate() is a nice shortcut for situations where you might be inclined to keep your own counter variable.
"""

# normally write like this
# lineno = 1
# for line in f:
#     # Process line
#     ...
#     lineno += 1

"""
But it's usually much more elegant(and less error prone) to use enumerate() instead
"""
# for lineno, line in enumerate(f):
#     # Process line
#     ...


data = [(1, 2), (3, 4), (5, 6), (7, 8)]

# Correct!
for n, (x, y) in enumerate(data):
    pass

# Error!
for n, x, y in enumerate(data):
    pass

