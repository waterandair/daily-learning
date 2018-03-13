#!/usr/bin/python
# -*- coding utf-8 -*-

import math


def my_abs(x):
    if not isinstance(x, (int, float)):
        raise TypeError("bad operand type")
    if x >= 0:
        return x
    else:
        return -x


print(my_abs(-7))
