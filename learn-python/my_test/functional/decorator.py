#!/usr/bin/python
# -*- coding utf-8 -*-
import functools


def log(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print('call %s():' % func.__name__)
        return func(*args, **kwargs)
    return wrapper


@log
def now():
    print('20171031')


now()


def logger(text):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print('%s %s():' % (text, func.__name__))
            return func(*args, **kwargs)
        return wrapper
    return decorator


@logger('DEBUG')
def today():
    print('2015-3_num_date_time-25')


today()
print(today.__name__)



