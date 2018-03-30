#!/usr/bin/python3
# -*- coding utf-8 -*-

"""
To return multiple values from a function, simply return a tuple
"""
def myfun():
    return 1, 2, 3

a, b, c = myfun()
print(a, b, c)  # 1 2 3