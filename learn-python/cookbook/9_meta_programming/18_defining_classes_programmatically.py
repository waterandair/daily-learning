#!/usr/bin/python3
# encoding utf-8
import types


def __init__(self, name, shares, price):
    self.name = name
    self.shares = shares
    self.price = price


def cost(self):
    return self.shares * self.price


cls_dict = {
    '__init__': __init__,
    'cost': cost
}

# make a class
Stock = types.new_class('Stock', (), {}, lambda ns: ns.update(cls_dict))
Stock.__module__ = __name__


s = Stock('ACME', 1, 2)
print(s)  # <__main__.Stock object at 0x7ff91cc21828>
print(s.cost())  # 2

