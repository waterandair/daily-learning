#!/usr/bin/python
# -*- coding utf-8 -*-

import os

print('Process (%s) start...' % os.getpid())

# fork()调用一次，返回两次，因为操作系统自动把当前进程（称为父进程）复制了一份（称为子进程），然后，分别在父进程和子进程内返回。
# 子进程永远返回0，而父进程返回子进程的ID。
# 一个父进程可以fork出很多子进程，所以，父进程要记下每个子进程的ID，而子进程只需要调用getppid()就可以拿到父进程的ID
pid = os.fork()

if pid == 0:
    print("this is child process (%s) and my parent is %s" % (os.getpid(), os.getppid()))
else:
    print("I(%s) created a child process (%s)." % (os.getpid(), pid))
