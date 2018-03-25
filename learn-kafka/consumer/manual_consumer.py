#!/usr/bin/python3
# -*- coding utf-8 -*-
from kafka import KafkaConsumer

"""
enable_auto_commit: 是否自动提交 offset 默认True
auto_offset_commit: 当发生 OffsetOutOfRange 时， 重置 offset 的策略，默认 latest
                    latest: 设置 offset 为最近一个消息，如果采用latest，消费者只能得道其启动后生产者生产的消息 
                    earliest: 设置 offset 为存在的时间最长的一条消息
consumer_timeout_ms： 获取不到消息等待的时间，超过这个值，就会抛出  StopIteration 异常
"""
consumer = KafkaConsumer(
    bootstrap_servers=[
        '172.17.0.2:9092',
        '172.17.0.3:9092',
        '172.17.0.4:9092',
    ],
    group_id='group-0',
    enable_auto_commit=False,
    auto_offset_reset='earliest',
    consumer_timeout_ms=1000
)

consumer.subscribe(["test"])

size = 10
while True:
    records_list = []
    for message in consumer:
        print("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition, message.offset, message.key, message.value))
        records_list.append(message)

    if len(records_list) > size:
        # 集中处理这一批消息，处理成功后，再提交 offset， 实现了 at least once 的语义
        # 异步提交 offset
        consumer.commit_async()
        # 清空 records_list
        records_list.clear()
