#!/usr/bin/python3
# -*- coding utf-8 -*-

import itertools

# count() 创建一个无限迭代器
natuals = itertools.count(1)

for n in natuals:
    print(n)
    if n > 100:
        break

c = itertools.cycle('abc')
t = 10
for i in c:
    print(i)
    t = t - 1
    if t == 0:
        break


r = itertools.repeat


