#!/usr/bin/python
# -*- coding utf-8 -*-
import os

# a very elegant way to combine a data reduction and a transformation is to use a generator-expression argument
# for example, if you want to calculate the sum of squares, do the following
nums = [1, 2, 3, 4, 5]
s = sum((x * x for x in nums))  # pass generator-expr as argument
s = sum(x * x for x in nums)  # more elegant syntax
print(s)

# determine if any .py files exist in a directory
files = os.listdir('./')
print(files)

if any(name.endswith('.py') for name in files):
    print('there be python!')
else:
    print('sorry, no python')

# output a tuple as csv
s = ('ACME', 50, 123.45)
print(','.join(str(x) for x in s))

# data reduction across fields of a data structure
portfolio = [
    {'name': 'kobe', 'points': 81},
    {'name': 'jordan', 'points': 64},
    {'name': 'ai', 'points': 65},
    {'name': 'wade', 'points': 63},

]
min_points = min(s['points'] for s in portfolio)
print(min_points)

# using a generator argument is often a more efficient and elegant approach than first creating
# a temporary list. For example, if you didn't use a generator expression, you might consider this
# alternative implementation

nums = [1, 2, 3, 4, 5]
s = sum([x * x for x in nums])

# this is works, but is introduces an extra step and creates an extra list.For such a small list,it might
# not matter,but if nums was huge, you would end up creating a large temporary data structure to only be
# used once and discarded.the generator solution transforms the data iteratively and is therefore mu
# much more memory-efficient


min_points = min(s['points'] for s in portfolio)
print(min_points)

min_points = min(portfolio, key=lambda s: s['points'])
print(min_points)



