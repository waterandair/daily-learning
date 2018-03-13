#!/usr/bin/python
# -*- coding utf-8 -*-

import threading

# 创建全局 Threadlocal 对象
# 一个ThreadLocal变量虽然是全局变量，但每个线程都只能读写自己线程的独立副本，互不干扰。
# ThreadLocal解决了参数在一个线程中各个函数之间互相传递的问题。
local_school = threading.local()


def process_student():
    # 获取当前线程关联的 student:
    std = local_school.student
    print("hello, %s in %s" % (std, threading.current_thread().name))


def process_thread(name):
    # 绑定 threadLocal 的 student
    local_school.student = name
    process_student()


t1 = threading.Thread(target=process_thread, args=("kobe",), name="Thread-A")
t2 = threading.Thread(target=process_thread, args=("wade",), name="Thread-B")

t1.start()
t2.start()

t1.join()
t2.join()
