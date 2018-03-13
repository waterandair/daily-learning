#!/usr/bin/python3
# coding utf-8
import threading
"""
Your program uses threads and you want to lock critical sections of code to avoid race conditions
To make objects safe to use by multiple threads, use Lock objects in the threading library
"""
class SharedCounter:
    """
    A counter object that can be shared by multiple threads.
    """
    def __init__(self, initial_value=0):
        self._value = initial_value
        self._value_lock = threading.Lock()

    def incr(self,delta=1):
        with self._value_lock:
            self._value += delta

    def decr(self, delta=1):
        with self._value_lock:
            self._value -= delta

