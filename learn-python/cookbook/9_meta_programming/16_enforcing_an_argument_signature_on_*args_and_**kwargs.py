#!/usr/bin/python3
# encoding utf-8
from inspect import Signature, Parameter
import inspect


def make_sig(*args):
    parms = [Parameter(name, Parameter.POSITIONAL_OR_KEYWORD) for name in args]
    return Signature(parms)


class Structure:
    __signature__ = make_sig()

    def __init__(self, *args, **kwargs):
        bound_values = self.__signature__.bind(*args, **kwargs)
        for name, value in bound_values.arguments.items():
            setattr(self, name, value)


class Stock(Structure):
    __signature__ = make_sig('name', 'shares', 'price')


class Point(Structure):
    __signature__ = make_sig('x', 'y')


print(inspect.signature(Stock))  # (name, shares, price)
print(inspect.signature(Point))  # (x, y)

s1 = Stock('acme', 100, 120)
# s2 = Stock('ac', '2')  # TypeError: missing a required argument: 'price'
# s3 = Stock('ACME', 100, 490.1, shares=50)  # multiple values for argument 'shares'


"""
In the last example of the solution, it might make sense to create signature objects through the use of a custom 
metaclass.
"""


class StructureMate(type):
    def __new__(cls, clsname, bases, clsdict):
        clsdict['__signature__'] = make_sig(*clsdict.get('_fields', []))
        return super().__new__(cls, clsname, bases, clsdict)


class Structure(metaclass=StructureMate):
    _fields = []

    def __init__(self, *args, **kwargs):
        bound_value = self.__signature__.bind(*args, **kwargs)
        for name, value in bound_value.arguments.items():
            setattr(self, name, value)


class Stock(Structure):
    _fields = ['name', 'shares', 'price']


class Point(Structure):
    _fields = ['x', 'y']

