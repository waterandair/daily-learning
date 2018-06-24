#!/usr/bin/ python3
# -*- coding: utf-8 -*-
"""
PerForking 异步 RPC 服务器
单个进程的IO能力有限,且python由于GIL的原因只能使用到一个CPU核心的资源,为了进一步提高并发能力,就应该使用多进程
Tornado 和 Nginx 就是采用了这种多进程异步模型
"""
import os
import json
import struct
import socket
import asyncore
from io import BytesIO


class RPCServer(asyncore.dispatcher):
    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(1)
        self.prefork(10)  # 创建10个子进程

    def prefork(self, n):
        for i in range(n):
            pid = os.fork()
            if pid < 0:  # fork error
                return
            if pid > 0:  # parent process
                continue
            if pid == 0:
                break  # child process

    def handle_accept(self):
        # 获取连接
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            # 处理连接
            RPCHandler(sock, addr)


class RPCHandler(asyncore.dispatcher_with_send):
    def __init__(self, sock, addr):
        asyncore.dispatcher_with_send.__init__(self, sock=sock)
        self.addr = addr
        self.handlers = {
            "ping": self.ping
        }
        self.rbuf = BytesIO()

    def handle_connect(self):
        print(self.addr, "comes")

    def handle_close(self):
        print(self.addr, "bye")
        self.close()

    def handle_read(self):
        while True:
            content = self.recv(1024)
            if content:
                # 追加到读缓冲
                self.rbuf.write(content)
            # 说明内核缓冲区空了，等待下个事件循环再继续读
            if len(content) < 1024:
                break
        self.handle_rpc()

    def handle_rpc(self):
        while True:
            self.rbuf.seek(0)
            length_prefix = self.rbuf.read(4)
            if len(length_prefix) < 4:
                break
            length, = struct.unpack("I", length_prefix)
            body = self.rbuf.read(length)
            if len(body) < length:
                break
            request = json.loads(body.decode())
            in_ = request['in']
            params = request['params']
            print(os.getpid(), in_, params)

            handler = self.handlers[in_]
            handler(params)
            # 截断读缓冲
            left = self.rbuf.getvalue()[length + 4:]
            self.rbuf = BytesIO()
            self.rbuf.write(left)
        self.rbuf.seek(0, 2)  # 移动游标到缓冲区末尾，便于后续内容直接追加

    def ping(self, params):
        self.send_result("pong", params)

    def send_result(self, out, result):
        response = {"out": out, "result": result}
        body = json.dumps(response)
        length_prefix = struct.pack("I", len(body))
        self.send(length_prefix)
        self.send(body.encode())


if __name__ == '__main__':
    RPCServer("localhost", 8080)
    asyncore.loop()
