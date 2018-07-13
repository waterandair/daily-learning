#!/usr/bin/ python3
# -*- coding: utf-8 -*-
"""preforking 同步模型"""
import os
import json
import struct
import socket
from threading import Thread


def prefork(nums):
    """预先创建指定数量的子进程"""
    for i in range(nums):
        pid = os.fork()
        if pid < 0:
            return
        elif pid > 0:
            continue  # 父进程继续循环,继续fork子进程
        else:  # pid == 0
            break  # 子进程退出循环处理请求


def ping(conn, params):
    send_result(conn, "pong", params)


def send_result(conn, out, result):
    response = json.dumps({"out": out, "result": result}).encode()
    length_prefix = struct.pack("I", len(response))
    conn.send(length_prefix)
    conn.sendall(response)


def loop(sock, handlers):
    while True:
        conn, addr = sock.accept()
        # handle_conn(conn, addr, handlers)
        Thread(target=handle_conn, args=(conn, addr, handlers)).start()


def handle_conn(conn, addr, hanlers):
    print(addr, "comes")
    while True:
        length_prefix = conn.recv(4)
        if not length_prefix:
            print(addr, "bye")
            break
        length, = struct.unpack("I", length_prefix)
        body = conn.recv(length).decode()
        request = json.loads(body)
        in_ = request["in"]
        params = request["params"]
        print(in_, params)

        handler = handlers[in_]
        handler(conn, params)


if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("localhost", 8080))
    sock.listen(1)

    # 开启 10个 子进程
    # prefork(10)
    prefork(1)

    handlers = {
        "ping": ping
    }
    loop(sock, handlers)


