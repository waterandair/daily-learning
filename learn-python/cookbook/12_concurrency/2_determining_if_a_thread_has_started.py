#!/usr/bin/python3
# coding utf-8
from threading import Thread, Event
import time
"""
Here is some sample code that uses an Event to coordinate the startup of a thread
"""
def countdown(n, started_evt):
    print("countdown starting")
    started_evt.set()  # 执行了这一步,主线程才会继续执行
    while n > 0:
        print('T-minus', n)
        n -= 1
        time.sleep(1)


started_evt = Event()
print('Launching countdown')
t = Thread(target=countdown, args=(10, started_evt))
t.start()

# wait for the thread to start
started_evt.wait()
print('countdown is running')

"""
同样的,子线程之间的同步也可以用 Event 
"""

def thread1(my_event):
    print("start thread1...")
    for i in range(1, 7):
        if i == 4:
            my_event.set()
        print(i)
        time.sleep(1)

def wait_for_thread1(my_event):
    my_event.wait()
    print("ok, we can start thread2...")

my_event = Event()
t = Thread(target=thread1, args=(my_event,))
t2 = Thread(target=wait_for_thread1, args=(my_event,))
t. start()
t2.start()
