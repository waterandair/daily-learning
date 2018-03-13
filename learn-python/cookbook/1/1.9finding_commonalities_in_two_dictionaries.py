#!/usr/bin/python3
# -*- coding utf-8 -*-

a = {
   'x': 1,
   'y': 2,
   'z': 3
}

b = {
   'w': 10,
   'x': 11,
   'y': 2
}

# find keys in common
print(a.keys() & b.keys())  # {'x', 'y'}

# find keys in a that art not in b
print(a.keys() - b.keys())  # {'z'}

# find (key, value) pairs in common
print(a.items() & b.items())  # {('y', 2)}


# these kinds of operations can also be used to alter or filter dictionary contents.
# make a new dictionary with certain keys removed
c = {key: a[key] for key in a.keys() - {'z', 'w'}}
print(c)  # {'x': 1, 'y': 2}

# dictionary keys also support common set operations such as unions, intersections, and differences