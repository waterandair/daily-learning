#!/usr/bin/python3
# -*- coding utf-8 -*-
from queue import Queue
from functools import wraps
"""
You're writing code that uses callback functions, but you're concerned about the proliferation of small functions
and mind boggling control flow.
You would like some way to make the code look more like a normal sequence of procedural steps.;

Callback functions can be inlined into a function using generrators and coroutines.
"""
def apply_async(func, args, *, callback):
    # Compute the result
    result = func(*args)

    # Invoke the callback with the result
    callback(result)


class Async:
    def __init__(self, func, args):
        self.func = func
        self.args = args


def add(x, y):
    return x + y

def inlined_async(func):
    @wraps(func)
    def wrapper(*args):
        f = func(*args)
        result_queue = Queue()
        result_queue.put(None)
        while True:
            result = result_queue.get()  # wait
            try:
                a = f.send(result)
                apply_async(a.func, a.args, callback=result_queue.put)
            except StopIteration:
                break
    return wrapper


@inlined_async
def test():
    r = yield Async(add, (2, 3))
    print(r)
    r = yield Async(add, ('hello', 'world'))
    print(r)
    for n in range(10):
        r = yield Async(add, (n, n))
        print(r)
    print('Goodbye')


test()

"""
5
helloworld
0s 
2
4
6
8
10
12_concurrency
14
16
18
Goodbye
"""