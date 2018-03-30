#!/usr/bin/python
# -*- coding utf-8 -*-
import math
from itertools import compress

# the easiest way to filter sequence data is often to use a list comprehension. 快于 filter, 快于迭代
mylist = [1, 4, -5, 10, -7, 2, 3, -1]
print([n for n in mylist if n > 0])  # [1, 4, 10, 2, 3]
print([n for n in mylist if n < 0])  # [-5, -7, -1]

# one potential downside of using a list comprehension is that it might produce a large result if the
# original input is large.
# if this is a concern, you can use generator expressions to produce the filtered values iteratively

pos = (n for n in mylist if n > 0)
print(pos)  # <generator object <genexpr> at 0x7fc410449af0>
for x in pos:
    print(x)
# 1
# 4
# 10
# 2
# 3


# sometimes, the filtering criteria cannot be easily expressed in a list comprehension or generator expression.
# for example, suppose that the filtering process involves exception handing or some other complicated detail.
# for this, put the filtering code into its own function and use the built-in filter() function.
values = ['1', '2', '-3', '-', '4', 'N/A', '5']
def is_int(val):
    try:
        int(val)
        return True
    except ValueError:
        return False


ivals = list(filter(is_int, values))
print(ivals)  # ['1', '2', '-3', '4', '5']


mylist = [1, 4, -5, 10, -7, 2, 3, -1]
print([math.sqrt(n) for n in mylist if n > 0])


# one variation on filtering involves replacing the values that don't meet the criteria with a new value
# instead of discarding them.

clip_neg = [n if n > 0 else 0 for n in mylist]
print(clip_neg)  # [1, 4, 0, 10, 0, 2, 3, 0]
clip_pos = [n if n < 0 else 0 for n in mylist]
print(clip_pos)  # [0, 0, -5, 0, -7, 0, 0, -1]


# another notable filtering tool is itertools.compress()
addresses = [
    '5412 N CLARK',
    '5148 N CLARK',
    '5800 E 58TH',
    '2122 N CLARK'
    '5645 N RAVENSWOOD',
    '1060 W ADDISON',
    '4801 N BROADWAY',
    '1039 W GRANVILLE',
]
counts = [0, 3, 10, 4, 1, 7, 6, 1]
more5 = [n > 5 for n in counts]
print(more5)  # [False, False, True, False, False, True, True, False]
more5 = list(compress(addresses, more5))
print(more5)  # ['5800 E 58TH', '4801 N BROADWAY', '1039 W GRANVILLE']
