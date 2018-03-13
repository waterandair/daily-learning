#!/usr/bin/python
# -*- coding utf-8 -*-


L = [
    'kobe',
    'wade',
    't-mac',
    'ai'
]

print('L[0:3] = ', L[0:3])
print('L[:3] = ', L[:3])
print('L[1:3] = ', L[1:3])
print('L[-2:] = ', L[-2:])

R = list(range(100))
print('R[:10] = ', R[:10])
print('R[-10:] = ', R[-10:])
print('R[10:20] = ', R[10:20])
# 0-10 步长为2
print('R[:10:2] = ', R[:10:2])
# 0-100 步长为5
print('R[::5] = ', R[::5])

