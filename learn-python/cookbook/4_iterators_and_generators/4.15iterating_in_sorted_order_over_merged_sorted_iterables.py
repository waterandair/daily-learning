#!/usr/bin/python
# -*- coding utf-8 -*-
import heapq

"""
You have a collection of sorted sequences and you want to iterate over a sorted sequence of them all merged together.
"""
a = [1, 4, 7, 10]
b = [2, 5, 6, 11]

for c in heapq.merge(a, b):
    print(c)


"""
1
2
4
5
6
7
10
11
"""

# with open('sorted_file_1', 'rt') as file1, open('sorted_file_2', 'rt') as file2, open('merged_file', 'wt') as outf:
#
#     for line in heapq.merge(file1, file2):
#         outf.write(line)

"""
The iterative nature of heapq.merge means that it never reads any of the supplied sequences all at once.
This means that you can use it on very long sequences with very little overhead.
"""

"""
It's important to emphasize that heapq.merge() requires that all of the input sequences already by sorted.
In particular, it does not first read all of the data into a heap or do any preliminary sorting.
"""