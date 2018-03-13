#!/usr/bin/python
# -*- coding utf-8 -*-

from multiprocessing import Process, Queue
import os, time, random

# 写数据进程的代码
def write(q):
    print('process to write: %s:' % os.getpid())
    for x in ['A', 'B', 'C']:
        print('put %s to queue...' % x)
        q.put(x)
        time.sleep(random.random())


# 读进程执行的代码
def read(q):
    print('process to read:', os.getpid())
    while True:
        x = q.get(True)
        print('get %s from queue' % x)


if __name__ == '__main__':
    # 父进程创建 queue 并传给子进程
    q = Queue()
    pw = Process(target=write, args=(q,))
    # pr = Process(target=read, args=(q,))
    # # 启动子进程 pw 写入
    pw.start()
    # # 启动子进程 pr 读取
    # pr.start()
    # # 等待 pw 结束
    # pw.join()
    # # pr 进程里是死循环，无法等待其结束，只能强行终止
    # pr.terminate()

    # pw.join()
    # 主进程读
    while True:
            x = q.get(True, 1)
            print('get %s from queue' % x)

