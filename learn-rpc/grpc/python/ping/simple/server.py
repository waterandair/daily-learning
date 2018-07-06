#!/usr/bin/ python3
# -*- coding: utf-8 -*-
import grpc
import time
import ping_pb2
import ping_pb2_grpc
from concurrent import futures


class PingCalculatorServicer(ping_pb2_grpc.PingCalculatorServicer):
    def Calc(self, request, ctx):
        # 在这里实现业务逻辑
        return ping_pb2.PingResponse(n=request.n)


def main():
    # 多线程服务器
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # 实例化 ping 服务类
    servicer = PingCalculatorServicer()
    # 注册本地服务
    ping_pb2_grpc.add_PingCalculatorServicer_to_server(servicer=servicer, server=server)
    # 监听端口
    server.add_insecure_port('127.0.0.1:8083')
    # 开始接收请求
    server.start()
    # 使用 ctrl+c 可以退出服务
    try:
        time.sleep(1000)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    main()