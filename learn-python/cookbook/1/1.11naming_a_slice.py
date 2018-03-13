#!/usr/bin/python
# -*- coding utf-8 -*-

record = '....................100          .......513.25     ..........'
cost = int(record[20:32]) * float(record[40:48])
print(cost)  # 51325.0
# instead of doing that why not name the slices like this:

SHARES = slice(20, 32)
PRICE = slice(40, 48)
cost = int(record[SHARES]) * float(record[PRICE])
print(cost)  # 51325.0

items = [0, 1, 2, 3, 4, 5, 6]
a = slice(2, 4)
print(type(a))  # <type 'slice'>
print(items[2:4])  # [2, 3]
print(items[a])  # [2, 3]
items[a] = [10, 11]
print(items)  # [0, 1, 10, 11, 4, 5, 6]
del items[a]
print(items)  # [0, 1, 4, 5, 6]

# if you have a slice instance s, you can get more information about it by looking
# at its s.start, s.stop, and s.step attributes,respectively
x = range(100)
a = slice(2, 6, 2)
print('a.start:', a.start, 'a.stop:', a.stop, 'a.step:', a.step)  # ('a.start:', 2, 'a.stop:', 6, 'a.step:', 2)
print(x[a])  # [2, 4]


# using indices(size) to avoid IndexError exceptions when indexing
a = slice(2, 1000, 2)
s = 'HelloWorld'
print(a.indices(len(s)))  # (2, 10, 2)
for i in range(*a.indices(len(s))):
    print(s[i])
# l
# o
# o
# l

for i in range(*(0, 10)):
    print(i)

