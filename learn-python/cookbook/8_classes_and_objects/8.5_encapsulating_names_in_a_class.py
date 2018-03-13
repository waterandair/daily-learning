#!/usr/bin/python3
# -*- coding utf-8 -*-

class A :
    def __init__(self):
        self._internal = 0  # An internal attribute
        self.public = 1  # A public attribute

    def public_method(self):
        # A public method
        pass

    def _internal_method(self):
        pass


class B:
    def __init__(self):
        self.__private = 0

    def __private_method(self):
        pass

    def public_method(self):
        self.__private_method()


"""
The use of double leading underscores causes the name to be mangled to something else.
Specifically, the private attributes in the preceding class get renamed to _B__private and _B__private method
"""
class C(B):
    def __init__(self):
        super(C, self).__init__()
        self.__private = 1  # does not override B.__private

    # Does not override B.__private_method()
    def __private_method(self):
        pass


"""
It should also be noted that sometimes you may want to define a variable that clashes with the name of a reserved word.
For this, you should use a single trailing underscore.
"""
lambda_ = 2.0