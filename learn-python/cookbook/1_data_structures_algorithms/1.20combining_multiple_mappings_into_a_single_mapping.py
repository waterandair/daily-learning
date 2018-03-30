#!/usr/bin/python3
# -*- coding utf-8 -*-
from collections import ChainMap
a = {'x': 1, 'z': 3}
b = {'y': 2, 'z': 4}

# now suppose you want to perform lookups where you have to check both dictionaries.
# An easy way to do this is to use the ChainMap class from the collections module.

c = ChainMap(a, b)
print(c['x'])  # 1
print(c['y'])  # 2
print(c['z'])  # 3

print(len(c))  # 3
print(list(c.keys()))  # ['x', 'y', 'z']
print(list(c.values()))  # [1, 2, 3]

# if there are duplicate keys, the values from the first mapping get used.

# operation that mutate the mapping always affect the first mapping listed

c['z'] = 10
c['w'] = 40
del c['x']
print(a)  # {'w': 40, 'z': 10}


# a ChainMap is particularly useful when working with scoped values such as variables in a programming
# language. In fact, there are methods that make this easy
values = ChainMap()
values['x'] = 1
# add a new mapping
values = values.new_child()
values['x'] = 2
# add a new mapping
values = values.new_child()
values['x'] = 3
print(values)  # ChainMap({'x': 3}, {'x': 2}, {'x': 1})
print(values['x'])  # 3

# discard last mapping
values = values.parents
print(values['x'])  # 2
values = values.parents
print(values['x'])  # 1

print(values)  # ChainMap({'x': 1})


# As an alternative to ChainMap, you might consider merging dictionaries together using the update() method.
a = {'x': 1, 'z': 3}
b = {'y': 2, 'z': 4}
b.update(a)
print(b)  # {'y': 2, 'x': 1, 'z': 3}

# this works , but it requires you to make a completely separate dictionary object(or destructively alter one
# of the existing dictionaries). Also is any of the original dictionaries mutate, the changes don't get reflected
# in the merged dictionary.

# A ChainMap uses the original dictionaries, so it doesn't have this behavior



