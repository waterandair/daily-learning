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

    @wraps(func)   # use wraps
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(func.__name__, end - start)
        return result

    return wrapper


"""
An important feature of the @wraps decorator is that it makes the wrapped function available to you in the
__wrapped__ attribute.
"""

