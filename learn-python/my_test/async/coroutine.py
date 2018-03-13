#!/usr/bin/python3
# -*- coding utf-8 -*-


# 生成器 消费者
def consumer():
    r = 'ppp'
    count = 0
    while True:
        n = yield r
        count += 1
        if not n:
            return
        print('[consumer] Consumer %s ...' % n)
        r = '200 ok'
        print(count)


# 生产者
def produce(c):
    c.send(None)
    n = 0
    while n < 5:
        n = n + 1
        print('[produce] Produce %s ...' % n)
        r = c.send(n)
        print('[produce] Consumer return: %s' % r)

    c.close()


c = consumer()
produce(c)