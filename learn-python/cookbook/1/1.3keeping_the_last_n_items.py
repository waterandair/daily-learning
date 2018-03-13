#!/usr/bin/python
# -*- coding utf-8 -*-
from collections import deque

# when writing code to search for items, it is common to use a generator function involving yield
def search(lines, parttern, history=5):
    previous_lines = deque(maxlen=history)
    for line in lines:
        if parttern in line:
            yield line, previous_lines
        previous_lines.append(line)


if __name__ == '__main__':
    with open('somefile.txt') as f:
        for line, prevlines in search(f, 'python', 5):
            for pline in prevlines:
                print(pline)
            print(line)
            print('-'*20)


# using deque(maxlen=N) creates a fixed-sized queue.
# when new items are added and the queue is full,the oldest item is automatically removed.
# although you could manually perform such operations on a list,the queue solution is
# far more elegant and runs a lot faster
q = deque(maxlen=3)
q.append(1)
q.append(2)
q.append(3)
print(q)  # deque([1, 2, 3], maxlen=3)
q.append(4)
print(q)  # deque([2, 3, 4], maxlen=3)
q.append(5)
print(q)  # deque([3, 4, 5], maxlen=3)


# a deque can be used whenever you need a simple queue structure
# adding or popping items from either end of a queue has O(1) complexity
# this is unlike a list where inserting or removing items from the front of the list is O(N)
# so use deque as much as possible
q = deque()
q.append(1)
q.append(2)
q.append(3)
print(q)
q.appendleft(4)
print('appendleft', q)
q.pop()
print('pop:', q)
q.popleft()
print('popleft:', q)


# more operations example

