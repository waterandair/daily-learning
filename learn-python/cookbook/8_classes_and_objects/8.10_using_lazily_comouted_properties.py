#!/usr/bin/python3
# -*- coding utf-8 -*-
import math
"""
You'd like to define a read-only attribute as a property that only gets computed on access.
However, once accessed, you'd like the value to be cached and not recomputed on each access
"""

"""
An efficient way to define a lazy attribute is through the use of a descriptor class:
"""
class LazyProperty:
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            value = self.func(instance)
            setattr(instance, self.func.__name__, value)
            return value


class Circle:
    def __init__(self, radius):
        self.radius = radius

    @LazyProperty
    def area(self):
        print('Compute area')
        return math.pi * self.radius ** 2

    @LazyProperty
    def perimeter(self):
        print('Computing perimeter')
        return 2 * math.pi * self.radius

"""
Carefully observe that the messages "Computing area" and "Computing perimeter" only appear once.
"""
c = Circle(4.0)
print(c.radius)  # 4.0

print(c.area)
"""
Compute area
50.26548245743669
"""
print(c.area)  # 50.26548245743669

print(c.perimeter)
"""
Computing perimeter
25.132741228718345
"""
print(c.perimeter)  # 25.132741228718345


"""
One possible downside to this recipe is that the computed value becomes mutable after it's created.
If that's a concern, you can use a  slightly less efficient implementation:
"""
def lazyproperty(func):
    name = '_lazy_' + func.__name__
    @property
    def lazy(self):
        if hasattr(self, name):
            return getattr(self, name)
        else:
            value = func(self)
            setattr(self, name, value)
            return value
    return lazy

