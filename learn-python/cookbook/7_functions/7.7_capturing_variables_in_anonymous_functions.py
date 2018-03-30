#!/usr/bin/python3
# -*- coding utf-8 -*-

x = 10
a = lambda y: x + y
x = 20
b = lambda y: x + y

print(a(10))  # 30
print(b(10))  # 30
"""
The problem here is that the value of x used in the lambda expression is a free variable that 
gets bound at runtime, not definition time.
Thus, the value of x in the lambda expressions is whatever the value of the x variable happens to be at the
time of execution
"""
x = 15
print(a(10))  # 25
x = 3
print(a(10))  # 13


"""
If you want an anonymous function to capture a value at the point of definition and keep it, include the value as 
a default value, like this:
"""
x = 10
a = lambda y, x=x: x + y
x = 20
b = lambda y, x=x: x + y

print(a(10))  # 20
print(b(10))  # 30


funcs = [lambda x: x+n for n in range(5)]
for f in funcs:
    print(f(0))
"""
4
4
4
4
4
"""

funcs = [lambda x, n=n: x+n for n in range(5)]
for f in funcs:
    print(f(0))
"""
0
1
2
3
4
"""