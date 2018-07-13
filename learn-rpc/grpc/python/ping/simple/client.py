#!/usr/bin/ python3
# -*- coding: utf-8 -*-
"""单线程客户端"""
import grpc
import ping_pb2
import ping_pb2_grpc


def main():
    channel = grpc.insecure_channel('localhost:8080')
    # 使用 stub
    client = ping_pb2_grpc.PingCalculatorStub(channel)
    # 调用吧
    for i in range(10):
        print(i, client.Calc(ping_pb2.PingRequest(n=str(i))).n)


if __name__ == '__main__':
    main()