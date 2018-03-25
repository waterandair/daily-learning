#!/usr/bin/python3
# -*- coding utf-8 -*-
import time
from kafka import SimpleProducer, SimpleClient

client = SimpleClient([
    "172.17.0.2:9092",
    "172.17.0.3:9092",
    "172.17.0.4:9092",
])

"""
异步模式下，producer不会马上把消息发送到 kafka，而是根据触发条件一批一批的发送
batch_send_every_n: 每一批消息累计的最大消息数
batch_send_every_t: 每一批消息最大累计时长
"""
producer = SimpleProducer(
    client=client,
    async=True,
    batch_send_every_n=20,
    batch_send_every_t=60
)

n = 1
while True:
    mes = 'this is a async message-' + str(n)
    producer.send_messages("test", mes.encode())
    n += 1
    time.sleep(1)
