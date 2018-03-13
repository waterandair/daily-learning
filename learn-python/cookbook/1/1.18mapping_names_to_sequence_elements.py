#!/usr/bin/python3
# -*- coding utf-8 -*-
from collections import namedtuple

Subscriber = namedtuple('Subscriber', ['addr', 'joined'])
sub = Subscriber('jones@example.com', '2012-10-19')
print(sub.addr, sub.joined)

# although an instance of a namedtuple looks like a normal class instance, it is interchangeable with a tuple
# and supports all of the usual tuple operations such as indexing and unpacking.
print(len(sub))
addr, joined = sub
print(addr, joined)

# a major use case for named tuples is decoupling your code from the position of the element it manipulates
def compute_cost(records):
    """
    illustrate: in this example, it's hard for us to understand the meaning of rec[1] * rec[2]
    """
    total = 0.0
    for rec in records:
        total += rec[1] * rec[2]
    return total


Stock = namedtuple('Stock', ['name', 'shares', 'price'])
def compute_cost(records):
    """
    illustrate: this example is more readable
    """
    total = 0.0
    for rec in records:
        s = Stock(*rec)
        total += s.shares * s.price
        return total


# one possible use of a namedtuple is as a replacement for a dictionary, which requires more space to store.
# Thus, if you are building large data structures involving dictionaries, use of a namedtuple will be more
# efficient. However, be aware that unlike a dictionary, a namedtuple is immutable.
s = Stock('ACME', 100, 123.45)
# s.shares = 75  # AttributeError: can't set attribute

# if you need to change any of the attributes, it can be done using the _replace() method of a nametuple instance
# which makes an entirely new namedtuple with specified values replaced
s._replace(shares=75)
print(s)  # Stock(name='ACME', shares=100, price=123.45)