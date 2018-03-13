#!/usr/bin/python3
# coding utf-8
import threading
from contextlib import contextmanager
"""
In multithreaded programs, a common source of deadlock is due to threads that attempt to acquire multiple locks at once.
For instance,if a thread acquires the first lock, but then blocks trying to acquire the second lock, that thread can
potentially block the progress of other threads and make the program freeze
"""
"""
one solution to deadlock avoidance is to assign each lock in the program a unique number, and to enforce an ordering 
rule that only allows multiple locks to be acquired in ascending order.
This is surprisingly easy to implement using a context manager as follows:
"""

_local = threading.local()


@contextmanager
def acquire(*locks):
    # sort locks by object identifier
    locks = sorted(locks, key=lambda x: id(x))

    # make sure lock order of previously acquired locks is not violated
    acquired = getattr(_local, 'acquired', [])
    if acquired and max(id(lock) for lock in acquired) >= id(locks[0]):
        raise RuntimeError('Lock Order Violation')

    # acquire all of the locks
    acquired.extend(locks)
    _local.acquired = acquired
    try:
        for lock in locks:
            lock.acquire()
        yield
    finally:
        # release locks in reverse order of acquisition
        for lock in reversed(locks):
            lock.release()
        del acquired[-len(locks):]


x_lock = threading.Lock()
y_lock = threading.Lock()


def thread_1():
    while True:
        with acquire(x_lock, y_lock):
            print('thread-1')


def thread_2():
    while True:
        with acquire(y_lock, x_lock):
            print('thread-2')


t1 = threading.Thread(target=thread_1)
t1.start()

t2 = threading.Thread(target=thread_2)
t2.start()