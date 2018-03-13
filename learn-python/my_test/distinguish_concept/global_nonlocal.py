#!/usr/bin/python
# -*- coding utf-8 -*-

# global x语句告诉Python在func的本地作用域内，要使用全局作用域中的变量x
x = 99


def func():
    x = 88


func()
print(x)     # 输出99

x = 99


def func():
    global x
    x = 88


func()
print(x)    # 输出88


# nonlocal关键字，就会告诉Python在foo函数中使用嵌套作用域中的变量count，因此对变量count进行修改时，会直接影响到嵌套作用域中的count变量，程序最后也就输出12了
def func():
    count = 1

    def foo():
        count = 12
    foo()
    print(count)


func()    # 输出1


def func():
    count = 1

    def foo():
        nonlocal count
        count = 12
    foo()
    print(count)


func()     # 输出12

# 使用global关键字修饰的变量之前可以并不存在，而使用nonlocal关键字修饰的变量在嵌套作用域中必须已经存在。

