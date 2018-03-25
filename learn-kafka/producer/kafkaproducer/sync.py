#!/usr/bin/python3
# -*- coding utf-8 -*-

from kafka import KafkaProducer
from kafka.errors import KafkaError
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
"""
producer = KafkaProducer(
    bootstrap_servers=[
        "172.17.0.2:9092",
        "172.17.0.3:9092",
        "172.17.0.4:9092",
    ],
)

# key 用于hash， 相同 key 的 value 提交到相同的 partition，key 的值默认为 None， 表示随机分配
res = producer.send(topic='test', value=b'this is a sync test', key=None)

# producer 默认是异步模式， 调用 send 函数返回对象的 get 方法，可以把异步模式转换为同步模式
try:
    record_metadata = res.get(timeout=10)

    # 获取成功返回响应的数据
    print(record_metadata.topic)
    print(record_metadata.partition)
    print(record_metadata.offset)
except KafkaError:
    # 处理异常
    pass
