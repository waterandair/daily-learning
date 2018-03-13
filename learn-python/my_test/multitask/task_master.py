#!/usr/bin/python
# -*- coding utf-8 -*-

import random, time, queue
from multiprocessing.managers import BaseManager

# 发送任务的队列
task_queue = queue.Queue()

# 接收结果的队列
result_queue = queue.Queue()

# 从 BaseManager 继承的 QueueManager:
class QueueManager(BaseManager):
    pass


# 把两个 queue 都注册到网络上，callable 参数关联了 queue 对象:
QueueManager.register('task_queue', callable=lambda: task_queue)
QueueManager.register('result_queue', callable=lambda: result_queue)

# 绑定端口 5000 , 设置验证码为 ‘123’
manager = QueueManager(address=('', 5000), authkey=b'123')

# 启动Queue:
manager.start()

# 获得通过网络访问的 queue 对象
# 当我们在一台机器上写多进程程序时，创建的Queue可以直接拿来用，但是，在分布式多进程环境下，
# 添加任务到Queue不可以直接对原始的task_queue进行操作，那样就绕过了QueueManager的封装，
# 必须通过manager.get_task_queue()获得的Queue接口添加。
task = manager.task_queue()
result = manager.result_queue()

# 放几个任务到 task_queue
for i in range(10):
    n = random.randint(0, 10000)
    print('put task:', n)
    task.put(n)

# 从 result 队列读取结果
for i in range(10):
    r = result.get(timeout=60)
    print('result:', r)

# 关闭
manager.shutdown()
print('master exit')

