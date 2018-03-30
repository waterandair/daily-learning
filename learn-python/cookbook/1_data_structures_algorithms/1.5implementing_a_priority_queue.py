#!/usr/bin/python
# -*- coding utf-8 -*-
# use the heapq module to implement a simple priority queue
import heapq


class PriorityQueue:
    def __init__(self):
        self.__queue = []  # create a empty heap
        self.__index = 0

    def push(self, item, priority):
        heapq.heappush(self.__queue, (-priority, self.__index, item))
        self.__index += 1

    def pop(self):
        return heapq.heappop(self.__queue)


class Item:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'Item({!r})'.format(self.name)


q = PriorityQueue()
q.push(Item('foo'), 1)
q.push(Item('bar'), 5)
q.push(Item('spam'), 4)
q.push(Item('grok'), 1)
print(q.pop())
print(q.pop())
print(q.pop())
print(q._PriorityQueue__queue)

list = [
    (-5, 1, 'a', 1),
    (-4, 2, 'a', 1),
    (-4, 3, 'a', 1),
    (-3, 4, 'a', 1),
    (-3, 4, 'b', 1),
    (-5, 1, 'a', 1),
]
heap = []

for x in list:
    heapq.heappush(heap, x)

print(heap)
print(heapq.heappop(heap))
print(heap)
print(heapq.heappop(heap))
print(heap)
print(heapq.heappop(heap))
print(heap)
print(heapq.heappop(heap))
print(heap)
print(heapq.heappop(heap))
print(heap)

# if you want to use this queue for communication between threads, you need to add appropriate locking and signaling


