#!/usr/bin/python3
# -*- coding utf-8 -*-
from functools import wraps
import logging
"""
Suppose yoy want to write a decorate that adds logging to a function, but allows the user to specify the logging level 
and other details as arguments.
"""
def logged(level, name=None, message=None):

    def decorate(func):
        logname = name if name else func.__module__
        log = logging.getLogger(logname)
        logmsg = message if message else func.__name__

        @wraps(func)
        def wrapper(*args, **kwargs):
            log.log(level, logmsg)
            return func(*args, **kwargs)
        return wrapper
    return decorate


@logged(logging.DEBUG)
def add(x, y):
    return x + y


@logged(logging.CRITICAL, 'example')
def spam():
    print('Spam!')


add(1, 2)
