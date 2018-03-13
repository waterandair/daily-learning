#!/usr/bin/python3
# -*- coding utf-8 -*-

"""
Normally, the inner variables of a closure are completely hidden to the outside world. However you can provide access
by writing accessor functions and attaching them to the closure as function attributes
"""
def sample():
    n = 0
    # Closure function
    def func():
        print('n=', n)

    # Accessor methods for n
    def get_n():
        return n

    def set_n(value):
        nonlocal n
        n = value

    func.get_n = get_n
    func.set_n = set_n
    return func


f = sample()
f()  # n= 0

f.set_n(10)
f()  # n= 10

print(f.get_n())  # 10