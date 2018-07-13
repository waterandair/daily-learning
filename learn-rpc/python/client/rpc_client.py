#!/usr/bin/ python3
# -*- coding: utf-8 -*-
"""rpc客户端"""
import json
import time
import struct
import socket


def rpc(sock, in_, params):
    # 根据协议构造请求
    request = json.dumps({"in": in_, "params": params})  # 序列化请求消息体
    length_prefix = struct.pack("I", len(request))  # 请求长度前缀, 将一个整数编码成 4 个字节的字符串, "I" 表示无符号的整数
    sock.send(length_prefix)
    sock.sendall(request.encode())  # sendall 会执行 flush

    # 根据协议解析响应
    res_length_prefix = sock.recv(4)  # 接收响应长度前缀
    length, = struct.unpack("I", res_length_prefix)
    body = sock.recv(length)  # 接收指定长度的响应消息体
    response = json.loads(body.decode())
    return response["out"], response["result"]  # 返回响应类型和结果


if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("localhost", 8080))
    addr, port = s.getsockname()
    print(addr, port)  # 打印出客户端的地址和占用的端口
    # 连续发送10个请求
    for i in range(5):
        time.sleep(1)
        out, result = rpc(s, "ping", "hello {}".format(i))
        print(out, result)
    s.close()
