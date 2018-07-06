#!/usr/bin/ python3
# -*- coding: utf-8 -*-
import grpc
import ping_pb2
import ping_pb2_grpc


def main():
    channel = grpc.insecure_channel("127.0.0.1:8083")
    # 使用 stub
    client = ping_pb2_grpc.PingCalculatorStub(channel=channel)
    # 调用
    for i in range(1000):
        print("ping", str(i), "pong", client.Calc(ping_pb2.PingRequest(n=str(i))).n)


if __name__ == '__main__':
    main()