#!/usr/bin/python3
# encoding utf-8
from inspect import signature
import logging
"""
here is a metaclass that rejects any class definition containing methods with mixed-case name
"""

#
# class NoMixedCaseMeta(type):
#     def __new__(cls, clsname, bases, clsdict):
#         for name in clsdict:
#             if name.lower() != name:
#                 raise TypeError('bad attribute name: ' + name)
#
#         return super().__new__(cls, clsname, bases, clsdict)
#
#
# class Root(metaclass=NoMixedCaseMeta):
#     pass
#
#
# class A (Root):
#     def foo_bar(self):
#         pass
#
#
# class B (Root):
#     # def fooBar(self):   # bad attribute name: fooBar
#     #     pass
#     pass


"""
as a more advanced and useful example, here is a metaclass that checks the definition of redefined methods to make sure
they have the same calling signature as the original method in the superclass
"""


class MatchSignaturesMeta(type):
    def __init__(self, clsname, bases, clsdict):
        super(MatchSignaturesMeta, self).__init__(clsname, bases, clsdict)
        # find definitions located further up the class hierarchy that make up the parents of self
        sup = super(self, self)
        for name, value in clsdict.items():
            if name.startswith('_') or not callable(value):
                continue

            prev_dfn = getattr(sup, name, None)
            if prev_dfn:
                prev_sig = signature(prev_dfn)
                val_sig = signature(value)
                if prev_sig != val_sig:
                    logging.warning('signature mismatch in %s. %s != %s', value.__qualname__, prev_sig, val_sig)


class Root(metaclass=MatchSignaturesMeta):
    pass


class A(Root):
    def foo(self, x, y):
        pass

    def spam(self, x, *, z):
        pass


class B(A):
    def foo(self, a, b):
        # WARNING:root:signature mismatch in B.foo. (self, x, y) != (self, a, b)
        pass
    





