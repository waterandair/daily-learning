#!/usr/bin/ python3
# -*- coding: utf-8 -*-
""" 单线程异步 RPC 服务器模型 使用 asyncore 包实现 (select 多路复用系统调用)"""
import asyncore
from io import BytesIO
import socket
import json
import struct


class RPCServer(asyncore.dispatcher):
    """服务器套接字处理器必须继承dispatcher"""
    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(1)

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            PRCHandler(sock, addr)


class PRCHandler(asyncore.dispatcher_with_send):
    """
    客户端套接字处理器必须继承 dispatcher_with_send
    """

    def __init__(self, sock, addr):
        asyncore.dispatcher_with_send.__init__(self, sock=sock)
        self.addr = addr
        self.handlers = {
            "ping": self.ping
        }
        # 因为是非阻塞的，所以可能一条消息经历了多次读取，所以这里用一个BytesIO缓冲区存放读取进来的数据
        self.rbuf = BytesIO()  # 读缓冲区由用户代码维护，写缓冲区由 asyncore 内部提供

    def ping(self, params):
        self.send_result("pong", params)

    def send_result(self, out, result):
        response = {"out": out, "result": result}
        body = json.dumps(response).encode()
        length_prefix = struct.pack("I", len(body))
        self.send(length_prefix)
        self.send(body)

    def handle_connect(self):
        """新的连接被accept 回调方法"""
        print(self.addr, 'comes')

    def handle_close(self):
        """连接关闭之前回调方法"""
        print(self.addr, 'bye')
        self.close()

    def handle_read(self):
        """有读事件到来时回调方法"""
        while True:
            content = self.recv(1024)
            if content:
                self.rbuf.write(content)
            # 最后一部分数据,读取后退出循环
            if len(content) < 1024:
                break
        self.handle_rpc()

    def handle_rpc(self):
        """将读到的消息解包并处理"""
        while True:  # 可能一次性收到了多个请求消息，所以需要循环处理
            self.rbuf.seek(0)
            length_prefix = self.rbuf.read(4)
            if len(length_prefix) < 4:  # 不足一个消息
                break
            length, = struct.unpack("I", length_prefix)
            body = self.rbuf.read(length)
            if len(body) < length:  # 不足一个消息
                break
            request = json.loads(body.decode())
            in_ = request['in']
            params = request['params']
            print(in_, params)
            handler = self.handlers[in_]
            handler(params)  # 处理消息
            left = self.rbuf.getvalue()[length + 4:]  # 消息处理完了，缓冲区要截断
            self.rbuf = BytesIO()
            self.rbuf.write(left)
        self.rbuf.seek(0, 2)  # 将游标挪到文件结尾，以便后续读到的内容直接追加


if __name__ == '__main__':
    RPCServer("localhost", 8080)
    asyncore.loop()