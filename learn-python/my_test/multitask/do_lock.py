#!/usr/bin/python
# -*- coding utf-8 -*-

import threading

balance = 0
lock = threading.Lock()


def change_it(n):
    global balance
    balance = balance + n
    balance = balance - n


def run_thread(n):
    for i in range(1000000):

        # 先要获取锁
        lock.acquire()
        try:
            change_it(n)
        finally:
            pass
            # 执行完后一定要释放锁
            lock.release()


t1 = threading.Thread(target=run_thread, args=(5,))
t2 = threading.Thread(target=run_thread, args=(8,))

t1.start()
t2.start()

t1.join()
t2.join()

print(balance)

"""
多线程编程，模型复杂，容易发生冲突，必须用锁加以隔离，同时，又要小心死锁的发生。
Python解释器由于设计时有GIL全局锁，导致了多线程无法利用多核。多线程的并发在Python中就是一个美丽的梦。
"""