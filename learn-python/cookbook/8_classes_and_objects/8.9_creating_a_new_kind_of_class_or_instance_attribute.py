#!/usr/bin/python3
# -*- coding utf-8 -*-

"""
If you want to crate an entirely new kind of instance attribute, define its functionality in the form of a
descriptor class
"""
# descriptor attribute for an integer type-checked attribute
class Integer:
    def __init__(self, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise TypeError('Expected an int')
        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        del instance.__dict__[self.name]


"""
To use a descriptor, instances of the descriptor are placed into a class definition as class variables
"""
class Point:
    x = Integer('x')
    y = Integer('y')
    def __init__(self, x, y):
        self.x = x
        self.y = y


"""
When you do this, all access to the descriptor attributes is captured by the __get__(), __set__, and __delete__()methods 
"""
p = Point(2, 3)
print(p.x)  # 2 (calls Point.x.__get__(p, Point))

p.y = 5  # Calls Point.y.__set__(p, 5)
# p.x = 2.3  # Calls Point.x.__set__(p, 2.3)  TypeError: Expected an int

# Does NOT work
"""
class Point:
    def __init__(self, x, y):
        self.x = Integer('x') # No! Must be a class variable
        self.y = Integer('y')
        self.x = x
        self.y = y
"""