#!/usr/bin/ python3
# -*- coding: utf-8 -*-
import socket


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("localhost", 8083))
    sock.sendall(b"ping")  # 将消息发送到 send buffer
    print(sock.recv(1024))  # 从 recv buffer 中读取响应
    sock.close()


if __name__ == '__main__':
    main()
