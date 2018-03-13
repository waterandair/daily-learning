#!/usr/bin/python3
# -*- coding utf-8 -*-
from functools import wraps
"""
Defining a decorator inside a class is straightforward, but you first need to sort out the manner in which the
decorator will be applied. Specifically, whether it is applied as an instance or a class method
Here is an example that
"""


class A:
    # decorator as an instance method
    def decorator1(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print('decorator 1')
            return func(*args, **kwargs)

    # decorator as a class method
    @classmethod
    def decorator2(cls, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print('decorator 2')
            return func(*args, **kwargs)
        return wrapper


# as an instance method
a = A()

@a.decorator1
def spam():
    pass

# as a class method
@A.decorator2
def grok():
    pass
