#!/usr/bin/python3
# -*- coding utf-8 -*-
from kafka import SimpleProducer, SimpleClient

client = SimpleClient([
    "172.17.0.2:9092",
    "172.17.0.3:9092",
    "172.17.0.4:9092",
])


"""
同步生产模式
client: SimpleProducer 客户端
async: 默认同步 False
req_acks: 服务器端返回响应的时机
        ACK_NOT_REQUIRED: 不需要返回响应
        ACK_AFTER_LOCAL_WRITE: 服务器写入 local log 后返回响应
        ACK_AFTER_CLUSTER_COMMIT: 消息提交到了集群中所有的副本后，返回响应
ack_timeout: 未接到响应，认为发送失败的时间
sync_fail_on_error: 抛出异常(True) 或 返回error(False) 
"""
producer = SimpleProducer(
    client=client,
    async=False,
    req_acks=SimpleProducer.ACK_NOT_REQUIRED,
    ack_timeout=2000,
    sync_fail_on_error=False
)

# 发送二进制数据
producer.send_messages("test", b"this a test")
# 一次发送多条消息
producer.send_messages("test", b"this a test-2", b"really test-2")
# 获取返回值ProduceResponsePayload对象
res = producer.send_messages("test", "这是一个测试".encode())
print(res)
for r in res:
    # 获取消息的 offset
    print(r.offset)



