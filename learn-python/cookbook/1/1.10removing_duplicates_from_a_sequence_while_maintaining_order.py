#!/usr/bin/python3
# -*- coding utf-8 -*-
from collections import Iterable, Iterator
# if the values in the sequence are hashable, the problem can be easily solved using a set and a generator.


def dedupe(items):
    seen = set()
    for item in items:
        if item not in seen:
            yield item
            seen.add(item)


a = [1, 5, 2, 1, 9, 1, 5, 10]
print(isinstance(dedupe(a), Iterator))  # True
print(list(dedupe(a)))  # [1, 5, 2, 9, 10]


# this only works if the items in the sequence are hashable.
# if you trying to eliminate duplicates in a sequence of unhashable types(such as dicts),you can make a slight change
# this latter solution also works nicely if you want to eliminate duplicates based on the value of a single
# field or attribute or a large data structure
def dedupe(items, key=None):
    seen = set()
    for item in items:
        val = item if key is None else key(item)
        if val not in seen:
            yield item
            seen.add(val)


a = [
    {'x': 1, 'y': 2},
    {'x': 1, 'y': 3},
    {'x': 1, 'y': 2},
    {'x': 2, 'y': 4}
]

print(list(dedupe(a, key=lambda d: (d['x'], d['y']))))  # [{'x': 1, 'y': 2}, {'x': 1, 'y': 3_num_date_time}, {'x': 2, 'y': 4}]

print(list(dedupe(a, key=lambda d: d['x'])))  # [{'x': 1, 'y': 2}, {'x': 2, 'y': 4}]

# if you want to read a file, eliminating duplicate lines, you could simply do this:
with open('./test.txt', 'r') as f:
    with open('./test2.txt', 'w') as target:
        for line in dedupe(f):
            target.writelines(line)


