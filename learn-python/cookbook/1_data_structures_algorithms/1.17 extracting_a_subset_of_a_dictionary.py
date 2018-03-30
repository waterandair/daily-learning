#!/usr/bin/python
# -*- coding utf-8 -*-

# you want to make a dictionary that is a subset of another dictionary

# this is easily accomplished using a dictionary comprehension.

prices = {
   'ACME': 45.23,
   'AAPL': 612.78,
   'IBM': 205.55,
   'HPQ': 37.20,
   'FB': 10.75
}

# make a dictionary of all prices over 200
p1 = {key: value for key, value in prices.items() if value > 200}
print(p1)  # {'AAPL': 612.78, 'IBM': 205.55}

# make a dictionary of tech stocks
tech_names = {'AAPL', 'IBM', 'HPQ', 'MSFT'}
p2 = {key: value for key, value in prices.items() if key in tech_names}
print(p2)  # {'HPQ': 37.2, 'AAPL': 612.78, 'IBM': 205.55}

# much of what can be accomplished with a dictionary comprehension might also be done by
# creating a sequence of tuples and passing them to dict() function
p1 = dict((key, value) for key, value in prices.items() if value > 200)
# However,the dictionary comprehension solution is a bit clearer and actually runs quite a bit
# faster(over twice)


# sometimes there are multiple ways of accomplishing the same thing.
# make a dictionary of tech stocks
tech_names = {'AAPL', 'IBM', 'HPQ', 'MSFT'}
p2 = {key: prices[key] for key in prices.keys() & tech_names}
# however, a timing study reveals that this solution is almost 1.6 times slower than the first solution
