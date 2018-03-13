#!/usr/bin/python3
# encoding utf-8
from abc import ABCMeta, abstractmethod


class IsStream(metaclass=ABCMeta):
    @abstractmethod
    def read(self, maxsize=None):
        pass

    @abstractmethod
    def write(self, data):
        pass


"""
In custom metaclass, additional keyword arguments can be supplied
To supplied such keyword arguments in a metacalss, make sure you define them on the 
__prepare()__, ___new__(), and __init__() methods using keyword-only arguments
"""
class MyMeta(type):
    # Optional
    @classmethod
    def __prepare__(cls, name, bases, debug=False, synchronize=False):
        # Custom processing
        return super().__prepare__(name, bases)

    # Required
    def __new__(cls, name, bases, ns, debug=False, synchronize=False):
        # Custom processing
        return super().__new__(cls, name, bases, ns)

    # Required
    def __init__(self, name, bases, ns, debug=False, synchronize=False):
        # Custom processing
        super().__init__(name, bases, ns)

