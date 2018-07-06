#!/usr/bin/ python3
# -*- coding: utf-8 -*-
import grpc
import time
import random
from concurrent import futures
import ping_pb2
import ping_pb2_grpc


class PingCalculatorServer(ping_pb2_grpc.PingCalculatorServicer):
    def Calc(self, request_iterator, ctx):
        # request 是一个迭代器参数,对应的是一个 stream 请求
        for request in request_iterator:
            # 50% 的概率会有响应, 为了演示请求和响应不是一对一的效果
            if random.randint(0, 1) == 1:
                continue
            # 响应是一个生成器, 一个响应对应一个请求
            yield ping_pb2.PingResponse(n=request.n)


def main():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    servicer = PingCalculatorServer()
    ping_pb2_grpc.add_PingCalculatorServicer_to_server(servicer, server)
    server.add_insecure_port("127.0.0.1:8083")
    server.start()

    try:
        time.sleep(1000)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    main()