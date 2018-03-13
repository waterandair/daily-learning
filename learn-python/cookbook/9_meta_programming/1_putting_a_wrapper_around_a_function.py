#!/usr/bin/python3
# -*- coding utf-8 -*-
import time
from functools import wraps

def timethis(func):
    """
    Decorator that reports the execution time
    :param func:
    :return:
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(func.__name__, end-start)
        return result
    return wrapper

@timethis
def countdown(n):
    while n > 0:
        n -=1

countdown(100000)  # countdown 0.004749298095703125

