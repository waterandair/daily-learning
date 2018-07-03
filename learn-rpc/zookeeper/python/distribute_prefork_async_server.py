#!/usr/bin/ python3
# -*- coding: utf-8 -*-
"""
分布式 RPC 服务
"""
import os
import sys
import json
import errno
import struct
import signal
import socket
import asyncore
import math
from io import BytesIO
from kazoo.client import KazooClient


class RPCServer(asyncore.dispatcher):
    zk_root = "/demo"
    zk_rpc = zk_root + "/rpc"

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.host = host
        self.port = port
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(1)
        self.child_pids = []
        # 创建子进程
        if self.prefork(10):
            # 父进程 注册 zookeeper 服务
            self.register_zk()
            # 父进程善后处理
            self.register_parent_signal()
        else:
            # 子进程善后处理
            self.register_child_signal()

    def prefork(self, n):
        """
        提前创建指定数量的子进程
        在父进程中返回 True, 子进程中返回 False
        :param n:
        :return:
        """
        for i in range(n):
            pid = os.fork()
            if pid < 0:
                # fork error
                raise RuntimeError()
            if pid > 0:
                # parent process, 记录子进程的 pid
                self.child_pids.append(pid)
                continue
            if pid == 0:
                # child process
                return False
        return True

    def register_zk(self):
        self.zk = KazooClient(hosts='127.0.0.1:2181')
        self.zk.start()
        # 创建根节点
        self.zk.ensure_path(self.zk_root)
        value = json.dumps({"host": self.host, "port": self.port})
        # 创建服务临时子节点, 路径后缀索引
        self.zk.create(self.zk_rpc, value, ephemeral=True, sequence=True)

    def register_parent_signal(self):
        """
        父进程监听的信号量
        :return:
        """
        signal.signal(signal.SIGINT, self.exit_parent)
        signal.signal(signal.SIGTERM, self.exit_parent)
        # 监听子进程退出
        signal.signal(signal.SIGCHLD, self.reap_child)

    def exit_parent(self):
        """
        父进程监听到 sigint 和 sigterm 信号, 关闭所有连接所有子进程
        :return:
        """
        # 关闭 zk 客户端
        self.zk.stop()
        # 关闭 serversocker
        self.close()
        # 关闭所有 clientsocket
        asyncore.close_all()
        pids = []
        # 关闭子进程
        for pid in self.child_pids:
            print("before kill")
            try:
                # 关闭子进程
                os.kill(pid, signal.SIGINT)
                pids.append(pid)
            except OSError as ex:
                # 目标子进程已经提前挂了
                if ex.args[0] == errno.ECHILD:
                    continue
                raise ex
            print("after kill ", pid)
        # 收割目标子进程
        for pid in pids:
            while True:
                try:
                    os.waitpid(pid, 0)
                    break
                except OSError as ex:
                    # 子进程已经被收割过了
                    if ex.args[0] == errno.ECHILD:
                        break
                    if ex.args[0] != errno.EINTR:
                        raise ex  # 被其它信号打断了,要重试
            print("wait over", pid)

    def reap_child(self):
        """
        父进程监听到 sigchld 信号, 退出子进程
        :param sig:
        :param frame:
        :return:
        """
        print("before reap")
        while True:
            try:
                # 收割任意子进程
                info = os.waitpid(-1, os.WNOHANG)
                break
            except OSError as ex:
                # 子进程已经被收割
                if ex.args[0] == errno.ECHILD:
                    return
                # 被其他信号打断要重试
                if ex.args[0] != errno.EINTR:
                    raise ex
        pid = info[0]
        try:
            self.child_pids.remove(pid)
        except ValueError:
            pass
        print("after reap", pid)

    def register_child_signal(self):
        signal.signal(signal.SIGINT, self.exit_child)
        signal.signal(signal.SIGTERM, self.exit_child)

    def exit_child(self):
        """
        子进程监听到 sigint 和 sigterm 信号, 关闭子进程所有连接
        :return:
        """
        # 关闭所有 server socket
        self.close()
        # 关闭所有 client socket
        asyncore.close_all()
        print("all closed")

    def handle_accept(self):
        # 接收新连接
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            RPCHandler(sock, addr)


class RPCHandler(asyncore.dispatcher_with_send):

    def __init__(self, sock, addr):
        asyncore.dispatcher_with_send.__init__(self, sock)
        self.addr = addr
        self.handlers = {
            "ping": self.ping,
            "pi": self.pi
        }
        self.rbuf = BytesIO()

    def handle_connect(self):
        print(self.addr, "comes")

    def handle_read(self):
        while True:
            connect = self.recv(1024)
            if connect:
                self.rbuf.write(connect)
                if len(connect) < 1024:
                    break
        self.handle_rpc()

    def handle_rpc(self):
        """
        接收一个完整的请求
        :return:
        """
        while True:
            self.rbuf.seek(0)
            length_prefix = self.rbuf.read(4)
            if len(length_prefix) < 4:
                break
            length, = struct.unpack("I", length_prefix)
            body = self.rbuf.read(length)
            if len(body) < length:
                break
            request = json.loads(body)
            in_ = request['in']
            params = request['params']
            print(os.getpid(), in_, params)
            handler = self.handlers[in_]
            handler(params)
            left = self.rbuf.getvalue()[length+4:]
            self.rbuf = BytesIO()
            self.rbuf.write(left)

    def ping(self, params):
        self.send_result("pong", params)

    def pi(self, n):
        s = 0.0
        for i in range(n + 1):
            s += 1.0 / (2 * i + 1) / (2 * i + 1)
        result = math.sqrt(8 * s)
        self.send_result("pi_r", result)

    def send_result(self, out, result):
        """
        给客户端发送消息
        :param out:
        :param result:
        :return:
        """
        response = {"out": out, "result": result}
        body = json.dumps(response)
        length_prefix = struct.pack("I", len(body))
        self.send(length_prefix)
        self.send(body)

    def handle_close(self):
        print(self.addr, "bye")
        self.close()


if __name__ == '__main__':
    host = sys.argv[1]
    port = int(sys.argv[2])
    RPCServer(host, port)
    # 启动事件循环
    asyncore.loop()
