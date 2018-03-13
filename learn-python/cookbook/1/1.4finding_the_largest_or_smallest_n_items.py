#!/usr/bin/python
# -*- coding utf-8 -*-

import heapq
nums = [1, 8, 2, 23, 7, -4, 18, 23, 42, 37, 2]
print(heapq.nlargest(3, nums))  # [42, 37, 23]
print(heapq.nsmallest(3, nums))  # [-4, 1, 2]

portfolio = [
   {'name': 'IBM', 'shares': 100, 'price': 91.1},
   {'name': 'AAPL', 'shares': 50, 'price': 543.22},
   {'name': 'FB', 'shares': 200, 'price': 21.09},
   {'name': 'HPQ', 'shares': 35, 'price': 31.75},
   {'name': 'YHOO', 'shares': 45, 'price': 16.35},
   {'name': 'ACME', 'shares': 75, 'price': 115.65}
]

cheap = heapq.nsmallest(2, portfolio, key=lambda s: s['price'])
expensive = heapq.nlargest(2, portfolio, key=lambda s: s['price'])
print(cheap)  # [{'price': 16.35, 'name': 'YHOO', 'shares': 45}, {'price': 21.09, 'name': 'FB', 'shares': 200}]
print(expensive)  # [{'price': 543.22, 'name': 'AAPL', 'shares': 50}, {'price': 115.65, 'name': 'ACME', 'shares': 75}]


# underneath the covers, they work by first converting the data into a list where items are order as a heap.
nums = [1, 8, 2, 23, 7, -4, 18, 23, 42, 37, 2]
heap = list(nums)
heapq.heapify(heap)
print(heap)

# heap[0] is always the smallest item.Moreover,subsequent items can be easily found using the heapq.heappop()method,
# which pops off the first item and replaces it with the next smallest item
print(heapq.heappop(heap))  # -4
print(heapq.heappop(heap))  # 1
print(heapq.heappop(heap))  # 2

print(heap)

# if you are simply trying to find the single smallest or largest item(N=1),it is faster to use min() and max()
print('max:', max(nums))  # 42
print('min:', min(nums))  # -4

# if N is about the same size as the collection itself,it is usually faster to sort it first and take a slice
print('sorted:', sorted(nums)[:10])



