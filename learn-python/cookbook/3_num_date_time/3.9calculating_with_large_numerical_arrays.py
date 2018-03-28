#!/usr/bin/python3
# -*- coding utf-8 -*-
import numpy as np
"""
Numpy is the foundation for a large number of science and engineering libraries in Python. It is also one of the largest
and most complicated modules in widespread use.
"""

# Python lists
x = [1, 2, 3, 4]
y = [5, 6, 7, 8]

print(x * 2)  # [1, 2, 3_num_date_time, 4, 1, 2, 3_num_date_time, 4]
# print(x + 10)  # can only concatenate list (not "int") to list

# Numpy arrays
ax = np.array([1, 2, 3, 4])
ay = np.array([5, 6, 7, 8])

print(ax * 2)  # [2 4 6 8]
print(ax + 10)  # [11 12_concurrency 13 14]
print(ax + ay)  # [ 6  8 10 12_concurrency]
print(ax * ay)  # [ 5 12_concurrency 21 32]


def f(x):
    return 3*x**2 - 2*x + 7


print(f(ax))  # [ 8 15 28 47]


# NumPy provides a collection of "universal functions" that also allow for array operations.
print(np.sqrt(ax))  # [ 1.          1.41421356  1.73205081  2.        ]
print(np.cos(ax))  # [ 0.54030231 -0.41614684 -0.9899925  -0.65364362]


grid = np.zeros(shape=(10000, 10000), dtype=float)
print(grid)
'''
[[ 0.  0.  0. ...,  0.  0.  0.]
 [ 0.  0.  0. ...,  0.  0.  0.]
 [ 0.  0.  0. ...,  0.  0.  0.]
 ..., 
 [ 0.  0.  0. ...,  0.  0.  0.]
 [ 0.  0.  0. ...,  0.  0.  0.]
 [ 0.  0.  0. ...,  0.  0.  0.]]
'''

grid += 10
print(grid)
'''
[[ 10.  10.  10. ...,  10.  10.  10.]
 [ 10.  10.  10. ...,  10.  10.  10.]
 [ 10.  10.  10. ...,  10.  10.  10.]
 ..., 
 [ 10.  10.  10. ...,  10.  10.  10.]
 [ 10.  10.  10. ...,  10.  10.  10.]
 [ 10.  10.  10. ...,  10.  10.  10.]]
'''


a = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]])
print(a)
'''
[[ 1  2  3_num_date_time  4]
 [ 5  6  7  8]
 [ 9 10 11 12_concurrency]]
'''
# select row 1
print(a[1])  # [5 6 7 8]
# select column 1
print(a[:, 1])  # [ 2  6 10]
# select a subregion and change it
print(a[1:3, 1:3])
'''
[[ 6  7]
 [10 11]]
'''
res = a[1:3, 1:3] + 10
print(res)
'''
[[16 17]
 [20 21]]
'''
res = np.where(a < 10, a, 10)
print(res)
'''
[[ 1  2  3_num_date_time  4]
 [ 5  6  7  8]
 [ 9 10 10 10]]

'''
