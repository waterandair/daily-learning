#!/usr/bin/python3
# -*- coding utf-8 -*-
from functools import partial

"""
 This recipe pertains to use of callback functions that are found in many libraries and frameworks,
 especially those related to asynchronous processing
"""
def apply_async(func, args, *, callback):
    # Compute the result
    result = func(*args)

    # Invoke the callback with the result
    callback(result)


def print_result(result):
    print('Got:', result)


def add(x, y):
    return x + y

apply_async(add, (2, 3), callback=print_result)  # Got: 5
apply_async(add, ('hello', 'world'), callback=print_result)  # Got: helloworld


"""1
One way to carry extra information in a callback is to use a bound-method instead of a simple function.
For example, this class keeps an internal sequence number that is incremented every time a result is received
"""
class ResultHandler:
    def __init__(self):
        self.sequence = 0

    def handler(self, result):
        self.sequence += 1
        print('[{}] Got: {}'.format(self.sequence, result))

r = ResultHandler()
apply_async(add, (2, 3), callback=r.handler)  # [1] Got: 5
apply_async(add, ('hello', 'world'), callback=r.handler)  # [2] Got: helloworld

"""2!!!
As an alternative to a class, you can also use a closure to capture state 
"""
def make_handler():
    sequence = 0
    def handler(result):
        nonlocal sequence
        sequence += 1
        print('[{}] Got: {}'.format(sequence, result))
    return handler

handler = make_handler()
apply_async(add, (2, 3), callback=handler)  # [1] Got: 5
apply_async(add, ('hello', 'world'), callback=handler)  # [2] Got: helloworld


"""3!!!coroutine
As yet another variation on this theme, you can sometimes use a coroutine to accomplish the same thing:
"""
def make_handler():
    sequence = 0
    while True:
        result = yield
        sequence += 1
        print('[{}] Got: {}'.format(sequence, result))

"""
for a coroutine, you would use its send() method as the callback:
"""
handler = make_handler()
next(handler)
apply_async(add, (1, 2), callback=handler.send)  # [1] Got: 3
apply_async(add, ('hello', 'world'), callback=handler.send)  # [2] Got: helloworld


"""4
Last, but not least, you can also carry state into a callback using an extra argument and partial function application
"""
class SequenceNo:
    def __init__(self):
        self.sequence = 0

def handler(result, seq):
    seq.sequence += 1
    print('[{}] Got: {}'.format(seq.sequence, result))

seq = SequenceNo()

apply_async(add, (2, 3), callback=partial(handler, seq=seq))
apply_async(add, ('hello', 'world'), callback=partial(handler, seq=seq))