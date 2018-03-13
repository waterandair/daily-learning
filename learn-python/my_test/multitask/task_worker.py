#!/usr/bin/python
# -*- coding utf-8 -*-

import time, sys, queue
from queue import Queue
from multiprocessing.managers import BaseManager

# 创建类似的 QueueManager:
class QueueManager(BaseManager):
    pass


QueueManager.register('task_queue')
QueueManager.register('result_queue')

# 连接到服务器，也就是运行 master 的 python 程序
server_addr = '127.0.0.1'
print('connect to server ', server_addr)

# 端口和验证码都要和 task_manager.py 设置的一致
manager = QueueManager(address=(server_addr, 5000), authkey=b'123')

# 从网络连接
manager.connect()

# 获取 queue 对象
task = manager.task_queue()
result = manager.result_queue()

# 从 task 队列中获取任务，把处理结果写入 result
for i in range(10):
    try:
        n = task.get(timeout=2)
        print('run task %s * %s' % (n, n))
        r = '%d * %d = %d' % (n, n, n * n)
        time.sleep(1)
        result.put(r)
    except Queue.Empty:
        print('task_queue is empty')

# 结束
print('worker exit')

