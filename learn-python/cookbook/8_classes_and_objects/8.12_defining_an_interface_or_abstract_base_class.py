#!/usr/bin/python3
# -*- coding utf-8 -*-
import io
from abc import ABCMeta, abstractmethod
"""
To define a abstract base class , use the abc module.
"""
class IStream(metaclass=ABCMeta):
    @abstractmethod
    def read(self, maxbytes=-1):
        pass

    @abstractmethod
    def write(self, data):
        pass


"""???
A central feature of an abstract base class is that it cannot be instantiated directly.
"""
# TypeError: Can't instantiate abstract class IStream with abstract methods read, write
# a = IStream()


"""
A major use of abstract base classes is in code that wants to enforce an expected programming interface.
"""

def serialize(obj, stream):
    if not isinstance(stream, IStream):
        raise  TypeError('Expected an IStream')
    pass


"""
ABCs allow other classes to be registered as implementing the required interface.
"""
# Register the built-in I/O classes as supporting our interface
IStream.register(io.IOBase)
f = open('foo.txt')
print(isinstance(f, IStream))  # True


"""
It should be noted that @abstractmethod can also be applied to static methods, class methods, and properties. 
You just need to make sure you apply it in the proper sequence where @abstractmethod appears immediately before 
the function definition, as shown here:
"""

class A(metaclass=ABCMeta):
    @property
    @abstractmethod
    def name(self):
        pass

    @name.setter
    @abstractmethod
    def name(self, value):
        pass

    @classmethod
    @abstractmethod
    def method1(cls):
        pass

    @staticmethod
    @abstractmethod
    def method2():
        pass