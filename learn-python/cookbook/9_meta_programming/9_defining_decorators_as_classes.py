#!/usr/bin/python3
# -*- coding utf-8 -*-
import types
from functools import wraps
"""
You want to wrap functions with a decorator, but the result is going to be a callable instance.
You need your decorator to work both inside and outside class definitions
To define a decorator as an instance, you need to make sure it implements the __call__() and __get__() methods
"""
class Profiled:
    def __init__(self, func):
        wraps(func)(self)
        self.ncalls = 0

    # 使类变成可调用对象
    def __call__(self, *args, **kwargs):
        self.ncalls += 1
        return self.__wrapped__(*args, **kwargs)

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            return types.MethodType(self, instance)


@Profiled
def add(x, y):
    return x + y


class Spam:
    @Profiled
    def bar(self, x):
        print(self, x)


print(add(2, 3))  # 5
print(add(4, 5))  # 9
print(add.ncalls)  # 2

s = Spam()
s.bar(1)  # <__main__.Spam object at 0x7f747481da20> 1
s.bar(2)  # <__main__.Spam object at 0x7f747481da20> 2
s.bar(3)  # <__main__.Spam object at 0x7f747481da20> 3

"""
If you want to avoid some of this mess, you might consider an alternative formulation of the decorator using closures
and nonlocal variables.
"""

def profiled(func):
    ncalls = 0
    @wraps(func)
    def wrapper(*args, **kwargs):
        nonlocal ncalls
        ncalls += 1
        return func(*args, **kwargs)

    wrapper.ncalls = lambda : ncalls
    return wrapper


@profiled
def add(x, y):
    return x + y

print(add(2, 3))
print(add(4, 5))
print(add.ncalls())

