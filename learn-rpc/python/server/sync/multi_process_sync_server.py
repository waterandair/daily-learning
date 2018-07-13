#!/usr/bin/ python3
# -*- coding: utf-8 -*-
"""多进程同步模型"""
import os
import json
import struct
import socket
import multiprocessing


def loop_multiprocessing(sock, handlers):
    """使用 multiprocessing 的方式为每一个连接创建一个新的进程进行处理"""
    while True:
        conn, addr = sock.accept()
        p = multiprocessing.Process(target=handler_conn, args=(conn, addr, handlers))
        p.start()


def loop_fork(sock, handlers):
    """使用fork的方式为每一个连接创建一个新的进程进行处理"""
    """
    子进程和父进程的关系:
        子进程创建后，父进程拥有的很多操作系统资源，会复制一份给子进程,比如套接字和文件描述符，它们本质上都是对操作系统内核对象的一个引用。
        如果子进程不需要某些引用，一定要即时关闭它，避免操作系统资源得不到释放导致资源泄露。

        进程 fork 之后，套接字会复制一份套接字连接到子进程，这时父子进程将会各有自己的套接字引用指向内核的同一份套接字对象。
        在子进程里对套接字进程 close，并不是关闭套接字，其本质上只是将内核套接字对象的引用计数减一,只有当引用计数减为零时，才会关闭套接字.
        所以关闭子进程的套接字后,要在父进程里也关闭客户端的套接字。
        否则就会导致服务器套接字引用计数不断增长，同时客户端套接字对象也得不到即时回收，造成资源泄露。
    """
    while True:
        conn, addr = sock.accept()
        pid = os.fork()  # fork 出一个子进程
        if pid < 0:  # 如果 fork 返回值小于零，一般意味着操作系统资源不足，无法创建进程。
            return
        elif pid > 0:  # fork在父进程的返回结果是一个大于0的整数值，这个值是子进程的进程号，父进程可以使用该进程号来控制子进程
            conn.close()  # 关闭父进程的客户端套接字,因为子进程已经复制了一份到子进程
            continue
        else:  # fork 在子进程的返回结果是零
            sock.close()  # 关闭子进程的服务器套接字, 因为只需要父进程保持套接字的监听
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
        # 获取当前运行程序的CPU核
        res = os.popen('ps -o psr -p' + str(os.getpid()))
        cpu_id = res.readlines()[1].rstrip("\n").strip()
        print(in_, params, "|", "from:", addr, "|", "cpu: " + cpu_id)
        handler = handlers[in_]
        handler(conn, params)


def ping(conn, params):
    send_result(conn, "pong", params)


def send_result(conn, out, result):
    response = json.dumps({"out": out, "result": result}).encode()
    length_prefix = struct.pack("I", len(response))
    conn.send(length_prefix)
    conn.sendall(response)


if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("localhost", 8080))
    sock.listen(1)
    handlers = {
        "ping": ping
    }

    # loop_multiprocessing(sock, handlers)  # python中提供了multiprocessing库去方面的进行多线程编程,这里使用fork是为了方便理解多进程
    loop_fork(sock, handlers)