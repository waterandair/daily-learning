#!/usr/bin/python3
# -*- coding utf-8 -*-

import threading
import asyncio

# 把一个generator标记为coroutine类型，然后在coroutine内部用yield from调用另一个coroutine实现异步操作
@asyncio.coroutine
def hello():
    print('hello world.', threading.currentThread())
    yield from asyncio.sleep(1)
    print('hello again', threading.currentThread())


loop = asyncio.get_event_loop()
tasks = [hello(), hello()]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()