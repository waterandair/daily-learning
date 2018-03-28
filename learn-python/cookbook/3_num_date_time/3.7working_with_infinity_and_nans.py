#!/usr/bin/python3
# -*- coding utf-8 -*-
import math
"""
Python has no special syntax to represent these special floating-point values, but they can be created using float()
"""
a = float('inf')
b = float('-inf')
c = float('nan')
print(a)  # inf
print(b)  # -inf
print(c)  # nan

# To text for the presence of these values, use the math.isinf() and math.isnan() functions
print(math.isinf(a))  # True
print(math.isnan(c))  # True

