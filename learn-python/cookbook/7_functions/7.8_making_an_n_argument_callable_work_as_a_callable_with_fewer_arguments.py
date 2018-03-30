#!/usr/bin/python3
# -*- coding utf-8 -*-
from functools import partial
"""
 If you need to reduce the number of arguments to a function, you should use functools.partial()
"""
def spam(a, b, c, d):
    print(a, b, c, d)

s1 = partial(spam, 1)   # a = 1
s1(2, 3, 4)  # 1, 2, 3, 4

s2 = partial(spam, 1, 2, d=42)
s2(3)  # 1 2 3 42
