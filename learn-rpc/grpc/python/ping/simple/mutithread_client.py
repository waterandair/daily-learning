#!/usr/bin/ python3
# -*- coding: utf-8 -*-
import grpc
import ping_pb2
import ping_pb2_grpc
from concurrent import futures


def ping(client, n):
    return client.Calc(ping_pb2.PingRequest(n=n)).n


def main():
    channel = grpc.insecure_channel('localhost:8083')
    client = ping_pb2_grpc.PingCalculatorStub(channel)
    # 线程池
    pool = futures.ThreadPoolExecutor(max_workers=10)
    results = []

    for i in range(100):
        print(i)
        results.append((i, pool.submit(ping, client, i)))

    pool.shutdown()


if __name__ == '__main__':
    main()