#!/usr/bin/python3
# -*- coding utf-8 -*-
import time
from kafka import KafkaProducer
import msgpack
import json

"""
bootstrap_servers: kafka 服务器地址
value_serializer: 指定用于序列化对象的方法 msgpack.dumps
                  eg.
                     producer = KafkaProducer(value_serializer=msgpack.dumps) 
                     producer.send('msgpack-topic', {'key': 'value'})

                     producer = KafkaProducer(value_serializer=lambda m: json.dumps(m).encode('ascii'))
                     producer.send('json-topic', {'key': 'value'})
retries: 重试次数
acks: 服务器端返回响应的时机
        0: 不需要返回响应
        1: 服务器写入 local log 后返回响应 (默认)
        all: 消息提交到了集群中所有的副本后，返回响应

异步模式下，producer不会马上把消息发送到 kafka，而是根据触发条件一批一批的发送，batch_size 和 linger_ms 满足其一，就会提交消息
batch_size: 每一批消息累计的最大消息数, 默认 16384
linger_ms: 每一批消息最大累计时长 默认0 ms
"""
producer = KafkaProducer(
    bootstrap_servers=[
        "172.17.0.2:9092",
        "172.17.0.3:9092",
        "172.17.0.4:9092",
    ],
    batch_size=5,
    linger_ms=3000
)
# key 用于hash， 相同 key 的 value 提交到相同的 partition，key 的值默认为 None， 表示随机分配
for i in range(100):
    mes = ('this is a async test ' + str(i)).encode()
    producer.send(topic='test', value=mes, key=None)
    time.sleep(1)

# block until all async messages are sent
producer.flush()
