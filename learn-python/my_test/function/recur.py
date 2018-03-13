#!/usr/bin/python
# -*- coding utf-8 -*-


# 递归计算阶乘
def fact(n):
    if n == 1:
        return 1
    return n * fact(n-1)


print(fact(5))


