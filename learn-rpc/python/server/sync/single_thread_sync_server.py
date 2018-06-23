#!/usr/bin/ python3
# -*- coding: utf-8 -*-
"""单线程同步模型rpc服务器"""
import json
import struct
import socket


def handle_conn(conn, addr, handlers):
    """
    接收并处理请求
    :param conn:
    :param addr:
    :param handlers:
    :return:
    """
    print(addr, "comes")
    # 循环读写
    while True:
        length_prefix = conn.recv(4)  # 接收请求长度
        if not length_prefix:  # 连接关闭了
            print(addr, "close")
            conn.close()
            break  # 退出循环,处理下一个连接

        length, = struct.unpack("I", length_prefix)
        body = conn.recv(length)  # 接收请求消息体
        request = json.loads(body.decode())
        in_ = request["in"]
        params = request["params"]
        print(in_, params)
        handler = handlers[in_]  # 找到请求处理器
        handler(conn, params)


def send_result(conn, out, result):
    """
    发送消息体
    :param conn:
    :param out:
    :param result:
    :return:
    """
    response = json.dumps({"out": out, "result": result})  # 构造响应消息体
    length_prefix = struct.pack("I", len(response))  # 编码响应长度前缀
    conn.send(length_prefix)
    conn.sendall(response.encode())  # sendall() 会执行 flush


def ping(conn, params):
    send_result(conn, "pong", params)


def loop(sock, handlers):
    """
    循环接收请求
    :param sock:
    :param handlers:
    :return:
    """
    while True:
        conn, addr = sock.accept()  # 接收连接
        handle_conn(conn, addr, handlers)


if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建一个基于 ipv4 的 TCP 套接字
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 在套接字级别打开 SO_REUSEADDR
    sock.bind(("localhost", 8080))
    sock.listen(1)  # 监听客户端连接

    # 注册请求处理器
    handlers = {
        "ping": ping
    }

    # 进入服务循环
    loop(sock, handlers)
