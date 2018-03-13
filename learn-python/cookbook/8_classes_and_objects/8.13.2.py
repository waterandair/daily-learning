#!/usr/bin/python3
# -*- coding utf-8 -*-

"""
As a final twist, a class decorator approach can also be used as a replacement for mixin classes, multiple
inheritance, and tricky use of the super() function.
Here is an alternative formulation of this recipe that uses class decorator
"""
class Descriptor:
    def __init__(self, name=None, **kwargs):
        self.name = name
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value


# Decorator for applying type checking
def typed(expected_type, cls=None):
    print(cls)
    if cls is None:
        return lambda cls: typed(expected_type, cls)

    super_set = cls.__set__

    def __set__(self, instance, value):
        print('1')
        if not isinstance(value, expected_type):
            raise TypeError('expected' + str(expected_type))
        super_set(self, instance, value)

    cls.__set__ = __set__
    return cls


# Decorator for unsigned values
def unsigned(cls):
    super_set = cls.__set__

    def __set__(self, instance, value):
        if value < 0:
            raise ValueError('Expected >= 0')
        super_set(self. instance, value)

    cls.__set__ = __set__
    return cls


# Decorator for allowing sized values
def maxsized(cls):
    super_init = cls.__init__

    def __init__(self, name=None, **kwargs):
        if 'size' not in kwargs:
            raise TypeError('missing size option')
        super_init(self, name, kwargs)
    cls.__init__ = __init__

    super_set = cls.__set__

    def __set__(self, instance, value):
        if len(value) >= self.size:
            raise ValueError('size must be < ' + str(self.size))
        super_set(self, instance, value)

    cls.__set__ = __set__
    return cls


# Specialized descriptors
@typed(int)
class Integer(Descriptor):
    pass


@unsigned
class UnsignedInteger(Integer):
    pass
#
#
# @typed(float)
# class Float(Descriptor):
#     pass
#
#
# @unsigned
# class UnsignedFloat(Float):
#     pass
#
# @typed(str)
# class String(Descriptor):
#     pass
#
# @maxsized
# class SizedString(String):
#     pass


class Test:
    name = Integer('name')

    def __init__(self, name):
        self.name = name

t = Test(1)
t.name = 'zj'