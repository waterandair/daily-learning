#!/usr/bin/ python3
# -*- coding: utf-8 -*-
"""多进程同步模型"""
"""
因为 Python 的 GIL 导致单个进程只能占满一个 CPU 核心,多进程并不能充分利用多核的优势,
所以多数 Python 服务器推荐使用多进程模型 
"""
import os
import json
import struct
import socket
import multiprocessing


def ping(conn, params):
    send_result(conn, "pong", params)


def send_result(conn, out, result):
    response = json.dumps({"out": out, "result": result}).encode()
    length_prefix = struct.pack("I", len(response))
    conn.send(length_prefix)
    conn.sendall(response)


def loop(sock, handlers):
    """
    使用 multiprocessing 库可以很方便的进行多进程编程
    :param sock:
    :param handlers:
    :return:
    """
    while True:
        conn, addr = sock.accept()
        p = multiprocessing.Process(target=handler_conn, args=(conn, addr, handlers))
        p.start()


def loop_fork(sock, handlers):
    """
    使用 os.fork() 的方式进行多进程编程,虽然比 multiprocessing 繁琐,但利于理解多进程
    :param sock:
    :param handlers:
    :return:
    """
    while True:
        conn, addr = sock.accept()
        """
        fork 调用将生成一个子进程，所以这个函数会在父子进程同时返回。
        在父进程的返回结果是一个整数值，这个值是子进程的进程号，父进程可以使用该进程号来控制子进程的运行。
        fork 在子进程的返回结果是零。
        如果 fork 返回值小于零，一般意味着操作系统资源不足，无法创建进程。
        
        子进程创建后，父进程拥有的很多操作系统资源，子进程也会持有。
        比如套接字和文件描述符，它们本质上都是对操作系统内核对象的一个引用。
        如果子进程不需要某些引用，一定要即时关闭它，避免操作系统资源得不到释放导致资源泄露。
        
        在子进程里关闭了服务器的套接字，同样要在父进程里关闭客户端的套接字。
        因为进程 fork 之后，套接字会复制一份到子进程，这时父子进程将会各有自己的套接字引用指向内核的同一份套接字对象。
        对套接字进程 close，并不是说就是关闭套接字，其本质上只是将内核套接字对象的引用计数减一。
        只有当引用计数减为零时，才会关闭套接字。
        如果没有上述逻辑就会导致服务器套接字引用计数不断增长，同时客户端套接字对象也得不到即时回收，这便是传说中的资源泄露。
        
        """
        pid = os.fork()  # fork 出一个子进程
        if pid < 0:  # fork error
            return
        elif pid > 0:  # 父进程
            conn.close()  # 关闭父进程的客户端套接字
            continue
        else:  # pid == 0, 子进程
            sock.close()  # 关闭子进程的服务器套接字
            handler_conn(conn, addr, handlers)
            break  # 处理完后一定要退出循环，不然子进程也会继续去 accept 连接


def handler_conn(conn, addr, handlers):
    print(addr, "comes")
    while True:
        length_prefix = conn.recv(4)
        if not length_prefix:
            print(addr, "bye")
            conn.close()
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
    handlers = {
        "ping": ping
    }

    # loop(sock, handlers)
    loop_fork(sock, handlers)