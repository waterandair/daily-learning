#!/usr/bin/ python3
# -*- coding: utf-8 -*-
import grpc
import ping_pb2
import ping_pb2_grpc


def generate_request():
    for i in range(1000):
        yield ping_pb2.PingRequest(n=i)


def main():
    channel = grpc.insecure_channel("127.0.0.1:8083")
    client = ping_pb2_grpc.PingCalculatorStub(channel)
    response_iterator = client.Calc(generate_request())
    # 请求是一个生成器,响应是一个迭代器
    for response in response_iterator:
        print("ping", response.n)


if __name__ == '__main__':
    main()