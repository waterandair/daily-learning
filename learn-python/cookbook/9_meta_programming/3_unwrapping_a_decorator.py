#!/usr/bin/python3
# -*- coding utf-8 -*-
import functools
"""
A decorator has been applied to a function, but you want to "undo" it, gaining access to the original unwrapped function
"""

def test(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print('test')
        res = func(*args, **kwargs)
        return res
    return wrapper


@test
def say_hello():
    print('hello')


# say_hello()

orig_say_hello = say_hello.__wrapped__
orig_say_hello()  # hello

