#!/usr/bin/python3
# -*- coding utf-8 -*-

"""
A simple way to customize access to an attribute is to define it as a "property".
For example, this code defines a property that adds simple type checking to an attribute
"""
class Person:
    def __init__(self, first_name):
        self.first_name = first_name

    # Getter function
    @property
    def first_name(self):
        return self._first_name

    # Setter function
    @first_name.setter
    def first_name(self, value):
        if not isinstance(value, str):
            raise TypeError('Expected a string')
        self._first_name = value

    # Deleter function (optional)
    @first_name.deleter
    def first_name(self):
        raise AttributeError("Can't delete attribute")


a = Person(12)  # TypeError: Expected a string
a = Person('Kobe')
print(a.first_name)  # Kobe (calls the getter)

# a.first_name = 42  #  TypeError: Expected a string

# del a.first_name  # AttributeError: Can't delete attribute