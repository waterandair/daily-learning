#!/usr/bin/ python3
# -*- coding: utf-8 -*-
"""分布式多进程 RPC 服务"""
import os
import sys
import json
import errno
import struct
import signal
import socket
import asyncore
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
            self.register_zk()  # 父进程 注册 zookeeper 服务
            self.register_parent_signal()  # 父进程善后处理
        else:
            self.register_child_signal()  # 子进程善后处理

    def prefork(self, n):
        """创建子进程 父进程中返回 True, 子进程返回 False"""
        for i in range(n):
            pid = os.fork()
            if pid < 0:
                raise RuntimeError()
            if pid > 0:
                self.child_pids.append(pid)  # 父进程,记录下子进程的pid
                continue
            if pid == 0:  # 子进程
                return False
        return True

    def register_zk(self):
        """父进程创建zookeeper连接"""
        self.zk = KazooClient(hosts='127.0.0.1:2181')
        self.zk.start()
        # 创建根节点
        self.zk.ensure_path(self.zk_root)
        value = json.dumps({"host": self.host, "port": self.port})
        # 创建服务临时子节点, 路径后缀索引
        self.zk.create(self.zk_rpc, value.encode(), ephemeral=True, sequence=True)

    def register_parent_signal(self):
        """父进程监听信号量"""
        signal.signal(signal.SIGINT, self.exit_parent)  # 监听父进程退出
        signal.signal(signal.SIGTERM, self.exit_parent)  # 监听父进程退出
        signal.signal(signal.SIGCHLD, self.reap_child)  # 监听子进程退出, 处理意外退出的子进程,避免僵尸进程

    def exit_parent(self, sig, frame):
        """父进程监听到 sigint 和 sigterm 信号, 关闭所有连接所有子进程"""
        self.zk.stop()  # 关闭 zk 客户端
        self.close()  # 关闭 serversocker
        asyncore.close_all()  # 关闭所有 clientsocket
        pids = []
        # 关闭子进程
        for pid in self.child_pids:
            print("before kill")
            try:
                os.kill(pid, signal.SIGINT)  # 关闭子进程
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
                    # 子进程退出后,父进程必须通过 waitpid 收割子进程,否则子进程会称为僵尸进程
                    os.waitpid(pid, 0)  # 收割目标子进程
                    break
                except OSError as ex:
                    # 子进程已经被收割过了
                    if ex.args[0] == errno.ECHILD:
                        break
                    if ex.args[0] != errno.EINTR:
                        raise ex  # 被其它信号打断了,要重试
            print("wait over", pid)

    def reap_child(self, sig, frame):
        """父进程监听到 sigchld 信号, 退出子进程"""
        print("before reap")
        while True:
            try:
                info = os.waitpid(-1, os.WNOHANG)  # 收割任意子进程
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
        """子进程监听信号"""
        signal.signal(signal.SIGINT, self.exit_child)  # 退出子进程
        signal.signal(signal.SIGTERM, self.exit_child)  # 退出子进程

    def exit_child(self, sig, frame):
        """子进程监听到 sigint 和 sigterm 信号, 关闭子进程所有连接"""
        self.close()  # 关闭所有 server socket
        asyncore.close_all()  # 关闭所有 client socket
        print("all closed")

    def handle_accept(self):
        """接收连接"""
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            RPCHandler(sock, addr)


class RPCHandler(asyncore.dispatcher_with_send):
    """处理请求"""
    def __init__(self, sock, addr):
        asyncore.dispatcher_with_send.__init__(self, sock)
        self.addr = addr
        self.handlers = {
            "ping": self.ping,
        }
        self.rbuf = BytesIO()

    def handle_connect(self):
        print(self.addr, "comes")

    def handle_read(self):
        """接收请求"""
        while True:
            connect = self.recv(1024)
            if connect:
                self.rbuf.write(connect)
                if len(connect) < 1024:
                    break
        self.handle_rpc()

    def handle_rpc(self):
        """处理一个接收一个完整的请求"""
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
            left = self.rbuf.getvalue()[length+4:]
            self.rbuf = BytesIO()
            self.rbuf.write(left)

    def ping(self, params):
        self.send_result("pong", params)

    def send_result(self, out, result):
        """给客户端发送消息"""
        response = {"out": out, "result": result}
        body = json.dumps(response)
        length_prefix = struct.pack("I", len(body))
        self.send(length_prefix)
        self.send(body.encode())

    def handle_close(self):
        print(self.addr, "bye")
        self.close()


if __name__ == '__main__':
    host = sys.argv[1]
    port = int(sys.argv[2])
    RPCServer(host, port)
    # 启动事件循环
    asyncore.loop()
