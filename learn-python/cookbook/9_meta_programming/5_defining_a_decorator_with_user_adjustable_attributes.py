#!/usr/bin/python3
# -*- coding utf-8 -*-
from functools import wraps, partial
import logging

"""
You want to write a decorator function that wraps a function, but has user adjustable attributes that can be used to
control the behavior of the decorator at runtime
"""


def attach_wrapper(obj, func=None):
    if func is None:
        return partial(attach_wrapper, obj)
    setattr(obj, func.__name__, func)
    return func


def logged(level, name=None, message=None):
    def decorate(func):
        logname = name if name else func.__module__
        log = logging.getLogger(logname)
        logmsg = message if message else func.__name__

        @wraps(func)
        def wrapper(*args, **kwargs):
            log.log(level, logmsg)
            return func(*args, **kwargs)

        # attach setter functions
        @attach_wrapper(wrapper)
        def set_level(newlevel):
            nonlocal level
            level = newlevel

        @attach_wrapper(wrapper)
        def set_message(newmsg):
            nonlocal logmsg
            logmsg = newmsg

        wrapper.get_level = lambda :level
        return wrapper
    return decorate


@logged(logging.DEBUG)
def add(x, y):
    return x + y


@logged(logging.CRITICAL, 'example')
def sapm():
    print('spam!')


logging.basicConfig(level=logging.DEBUG)
add(2, 3)  # DEBUG:__main__:add

add.set_message('Add called')
add(2, 3)  # DEBUG:__main__:Add called

add.set_level(logging.WARNING)
add(2, 3)  # WARNING:__main__:Add called

print(add.get_level())