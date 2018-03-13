#!/usr/bin/python3
# coding utf-8
from queue import Queue
from threading import Thread, Condition, Event
import heapq


# A thread that produces data
def producer(out_q):
    while True:
        # produce some data
        out_q.put('data')


# a thread that consums data
def consumer(in_q):
    while True:
        # get some data
        data = in_q.get()


# create the shared queue and launch both threads
q = Queue()
t1 = Thread(target=consumer, args=(q, ))
t2 = Thread(target=producer, args=(q, ))
t1.start()
t2.start()

"""
Queue instances already have all of the required locking, so they can be safely shared by as many threads as you wish

when using queues, it can be somewhat tricky to coordinate the shutdown of the producer and consumer.A common solution 
to this problem is to rely on a special sentinel value, which when placed in the queue, causes consumers to terminate.
"""


"""
Although queues are the most common thread communication mechanism, you can build your own data structures as long as 
you add the required locking and synchronization.The most common way to do this is to wrap your data structures with a 
condition variable.
Here is how you might build a thread-safe priority queue
"""
class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._count = 0
        self._cv = Condition()

    def put(self, item, priority):
        with self._cv:
            heapq.heappush(self._queue, (-priority, self._count, item))
            self._count += 1
            self._cv.notify()

    def get(self):
        with self._cv:
            while len(self._queue) == 0:
                self._cv.wait()
            return heapq.heappop(self._queue)[-1]


# Wait for all produced items to be consumed
q.join()
"""
If a thread needs to know immediately when a consumer thread has processed a particular item of data, you should pair 
sent data with an Event object that allows the producer to monitor its progress
"""
def producer2(out_q):
    while True:
        # produce some data
        # make an (data, enent) pair and hand it to the consumer
        evt = Event()
        out_q.put(('data', evt))
        # wait for the consumer to process the item
        evt.wait()


# a thread that consumes data
def consumer(in_q):
    while True:
        # get some data
        data, evt = in_q.get()
        # indicate completion
        evt.set()


"""
there are utility methods q.size(), q.full(), q.empty() that can tell you the current size and status of the queue.
However, be aware that all of these are unreliable in a multithreaded environment.
Frankly, it's best to write your code not to rely on such functions.
"""




