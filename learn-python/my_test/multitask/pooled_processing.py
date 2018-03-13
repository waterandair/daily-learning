#!/usr/bin/python
# -*- coding utf-8 -*-

from multiprocessing import Pool
import os, time, random


def long_time_task(name):
    print("run task %s(%s)..." % (name, os.getpid()))
    start = time.time()
    time.sleep(random.random() * 3)
    end = time.time()
    print('Task %s runs %0.2f seconds' % (name, (end - start)))


if __name__ == '__main__':
    print('parent process %s' % os.getpid())
    p = Pool(4)
    for i in range(6):
        p.apply_async(long_time_task, args=('process' + str(i),))
    print('waiting for all subprocess done...')
    p.close()
    p.join()
    print('all subprocess done')
