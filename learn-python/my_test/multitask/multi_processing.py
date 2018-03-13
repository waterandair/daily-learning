#!/usr/bin/python
# -*- coding utf-8 -*-

from multiprocessing import Process
import os
# 使用process方法可以做到跨平台（包括windows）

def run_proc(name):
    """子进程要执行的代码"""
    print("run child process %s (%s)..." % (name, os.getpid()))
    return 'ok'


if __name__ == '__main__':
    print('parent process %s.' % os.getpid())
    p = Process(target=run_proc, args=('test',))
    print('child process will start')
    p.start()
    p.join()  # join()方法可以等待子进程结束后再继续往下运行，通常用于进程间的同步
    print('child process end')

