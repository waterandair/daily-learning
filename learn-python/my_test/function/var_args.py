#!/usr/bin/python
# -*- coding utf-8 -*-


def greeting(greetings, *args):
    if len(args) == 0:
        print("%s" % greetings)
    else:
        print("%s, %s!" % (greetings, ', '.join(args)))


greeting('Hi')
greeting('Hi', 'kobe')
greeting('Hi', 'KOBE', 'WADE', 'T-MAC')

# names 是 tuple 或 list 都可以
names = ['kobe', 'wade', 't-mac']
greeting('Hi', *names)
