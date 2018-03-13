#!/usr/bin/python3
# -*- coding UTF-8 -*-
import time
from threading import Thread
import socket
"""
The threading library can be used to execute any Python callable in its own thread.To do this, 
you create a Thread instance and supply the callable that you wish to execute as a target. 
"""
def countdown(n):
    while n > 0:
        print('T-minus', n)
        n -= 1
        time.sleep(1)


def test_alive(t):
    """
    query a thread instance to see if it's still running
    :param t:
    :return:
    """
    if t.is_alive():
        print('still running')
    else:
        print('completed')


# Create and launch a thread
t = Thread(target=countdown, args=(10,))
"""
once start,threads run independently until the target function returns
"""
# t.start()
#
# time.sleep(5)
# test_alive(t)
# # you can also request to join with a thread, which waits for it to terminate
# # 可以将一个线程加入到当前线程,并等待它执行完
# t.join()
# test_alive(t)


"""
the interpreter remains running until all threads terminate.For long-running threads or background tasks that run 
forever, you should consider making the thread daemonic.
"""
t = Thread(target=countdown, args=(10,), daemon=True)
t.start()
"""
Daemonic threads can’t be joined.However, the are destroyed automatically when the main thread terminates.
后台线程不能being等待,主线程结束,后台线程也会跟着结束
"""


class CountdownTask:
    """
    You might put your thread in a class such as this:
    """
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def run(self, n):
        while self._running and n > 0:
            print ('T-minus', n)
            n -= 1
            time.sleep(1)


c = CountdownTask()
t = Thread(target=c.run, args=(10,))
t.start()
time.sleep(3)
c.terminate()  # Signal termination
t.join()  # Wait for actual termination (if needed)


"""
A thread to blocked indefinitely on an I/O operation may never return to check if it's been killed.
To correctly deal with this case, you'll need to careful program thread to utilize
timeout loops
"""


class IOTask:
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def run(self, sock):
        # sock is a socket
        sock.settimeout(5)  # Set timeout period
        while self._running:
            # Perform a blocking I/O operation w/ timeout
            try:
                data = sock.recv(8192)
                break
            except socket.timeout:
                continue
            # Continued processing
            pass
        # Terminated
        return


"""
由于全局解释锁（GIL）的原因，Python 的线程被限制到同一时刻只允许一个线程执行这样一个执行模型。
所以，Python 的线程更适用于处理I/O和其他需要并发执行的阻塞操作（比如等待I/O、等待从数据库获取
数据等等），而不是需要多处理器并行的计算密集型任务。
"""

"""
Sometimes you will see threads defined via inheritance from the Thread class
这样写不是不可以,缺点是使代码强依赖于 threading 库
"""
class CountdownThread(Thread):
    def __init__(self, n):
        super(CountdownThread, self).__init__()
        self.n = n

    def run(self):
        while self.n > 0:
            print('T-minus', self.n)
            self.n -= 1
            time.sleep(1)

c = CountdownThread(5)
c.start()