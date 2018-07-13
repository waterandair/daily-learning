#!/usr/bin/ python3
# -*- coding: utf-8 -*-
"""并行客户端"""
import grpc
import ping_pb2
import ping_pb2_grpc
from concurrent import futures


def ping(client, n):
    return client.Calc(ping_pb2.PingRequest(n=str(n))).n


def main():
    channel = grpc.insecure_channel("127.0.0.1:8080")
    client = ping_pb2_grpc.PingCalculatorStub(channel=channel)
    pool = futures.ThreadPoolExecutor(max_workers=4)  # 客户端使用线程池执行
    results = []
    for i in range(10):
        results.append((i, pool.submit(ping, client, str(i))))

    # 等待所有任务执行完毕
    pool.shutdown()

    for i, future in results:
        print(i, future.result())


if __name__ == '__main__':
    main()