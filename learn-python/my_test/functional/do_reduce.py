#!/usr/bin/python
# -*- coding utf-8 -*-

# reduce把一个函数作用在一个序列[x1, x2, x3, ...]上，这个函数必须接收两个参数，reduce把结果继续和序列的下一个元素做累积计算

from functools import reduce


CHAR_TO_INT = {
    '0': 0,
    '1': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9
}


def str2int(s):
    ints = map(lambda ch: CHAR_TO_INT[ch], s)
    # 使用了 list(ints) 后，发现后面 ints 变量就变成 None 了
    # print('ints:', list(ints))
    # print(ints)
    return reduce(lambda x, y: x * 10 + y, ints)


print(str2int('0'))
print(str2int('12300'))
print(str2int('0012345'))

CHAR_TO_FLOAT = {
    '0': 0,
    '1': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    '.': -1
}


def str2float(s):
    nums = map(lambda ch: CHAR_TO_FLOAT[ch], s)
    point = 0

    def to_float(f, n):
        nonlocal point
        if n == -1:
            point = 1
            return f
        if point == 0:
            return f * 10 + n
        else:
            point = point * 10
            return f + n / point
    return reduce(to_float, nums, 0.0)


print(str2float('0'))
print(str2float('123.456'))
print(str2float('123.45600'))
print(str2float('0.123'))  # 0.12300000000000001    ???
print(str2float('.1234'))
print(str2float('120.0034'))
