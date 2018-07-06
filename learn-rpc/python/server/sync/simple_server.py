#!/usr/bin/ python3
# -*- coding: utf-8 -*-
import socket


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 打开一个ipv4的tcp套接字
    sock.bind(("localhost", 8083))
    sock.listen(1)  # 监听客户端连接
    try:
        while True:
            conn, addr = sock.accept()  # 接收一个客户端连接
            print(conn.recv(1024))  # 从 recv buffer中读取消息
            conn.sendall(b"pong")  # 将响应发送到 send buffer
            conn.close()
    except KeyboardInterrupt:
        sock.close()


if __name__ == '__main__':
    main()
