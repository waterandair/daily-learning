#!/usr/bin/python3
# encoding utf-8
import time
from contextlib import contextmanager

"""
In the timethis() function, all of the code prior to the 'yield' executes as the __enter__()
method of a context manager.All of the code after the yield executes as the __exit__() method.
If there was an exception, it is raised at the yield statement.
"""


@contextmanager
def timethis(label):
    start = time.time()
    try:
        yield
    finally:
        end = time.time()
        print('{}: {}'.format(label, end - start))


with timethis('counting'):
    n = 10000000
    while n > 0:
        n -= 1



