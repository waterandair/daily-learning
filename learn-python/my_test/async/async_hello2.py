#!/usr/bin/python3
# -*- coding utf-8 -*-

import threading
import asyncio
# 为了简化并更好地标识异步IO，从Python 3.5开始引入了新的语法async和await，可以让coroutine的代码更简洁易读。
# 把@asyncio.coroutine替换为async；
# 把yield from替换为await。

async def hello():
    print('hello world ',threading.currentThread())
    await asyncio.sleep(1)
    print('hello again ', threading.currentThread())


loop = asyncio.get_event_loop()
tasks = [hello(), hello()]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()