#!/usr/bin/python3
# encoding utf-8

"""
You want to inspect or rewrite portions of a class definition to alter its behavior,
but without using inheritance or metaclasses
This might be a perfect use for a class decorator
"""
def log_getattribute(cls):
    # Get the original implementation
    orig_getattribute = cls.__getattribute__

    # make a new definition
    def new_getattribute(self, name):
        print('getting:', name)
        return orig_getattribute(self, name)

    # Attach to the class and return
    cls.__getattribute__ = new_getattribute
    return cls


@log_getattribute
class A:

    def __init__(self, x):
        self.x = x

    def spam(self):
        pass


a = A(42)
a.x  # getting: x
a.spam()  # getting: spam

