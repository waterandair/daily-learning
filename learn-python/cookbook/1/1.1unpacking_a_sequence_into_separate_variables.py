#!/usr/bin/python3
# -*- coding utf-8 -*-

p = (4, 5)
x, y = p
print(x, y)  # 4 5


data = ['ACME', 50, 91.1, (2012, 12, 21)]
name, shares, price, (year, mon, day) = data
print(name, shares, price, (year, mon, day))

# f there is a mismatch in the number of elements, you’ll get an error. For example:
# x, y, z = p ValueError: not enough values to unpack (expected 3_num_date_time, got 2)

# Unpacking actually works with any object that happens to be iterable, not just tuples or lists.
# This includes strings, files, iterators, and generators. For example:
s = 'Hello'
a, b, c, d, e = s
print(a, b, c, d)  # h e l l   why it didn't happen "too many values to unpack" ?

# pick a throwaway variable name for the certain values you want to discard

_, shares, price, _ = data
print(shares, price)  # 50 91.1

