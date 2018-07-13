#!/usr/bin/ python3
# -*- coding: utf-8 -*-
import json
import time
import struct
import socket
import random
from kazoo.client import KazooClient

zk_root = "/demo"
# 全局变量,RemoteServer 对象列表
G = {"servers": None}


def random_server():
    """随机获取一个服务节点"""
    if G["servers"] is None:
        # 首次初始化服务列表
        get_servers()
    if not G["servers"]:
        return
    return random.choice(G["servers"])


def get_servers():
    """服务发现 获取服务节点列表"""
    zk = KazooClient(hosts="127.0.0.1:2181")
    zk.start()
    # 当前活跃地址列表
    current_addrs = set()

    def watch_servers(*args):
        """服务变更通知 监听服务列表变更"""
        new_addrs = set()
        # 获取新的服务地址列表,并支持监听服务列表变动
        for child in zk.get_children(zk_root, watch=watch_servers):
            node = zk.get(zk_root + "/" + child)
            addr = json.loads(node[0].decode())
            new_addrs.add("{}:{}".format(addr["host"], addr["port"]))

        del_addrs = current_addrs - new_addrs  # # 服务列表变更后,原列表中要删除的服务地址
        del_servers = []

        # 服务列表变更后,原列表要删除的RemoteServerr对象
        for addr in del_addrs:
            for s in G["servers"]:
                if s.addr == addr:
                    del_servers.append(s)
                    break

        # 删除待删除的RemoteServer
        for server in del_servers:
            G["servers"].remove(server)
            current_addrs.remove(server.addr)

        add_addrs = new_addrs - current_addrs  # 新增的地址
        # 新增server
        for addr in add_addrs:
            G["servers"].append(RemoteServer(addr))
            current_addrs.add(addr)

    # 获取节点列表并持续监听服务列表变更
    for child in zk.get_children(zk_root, watch=watch_servers):
        node = zk.get(zk_root + "/" + child)
        addr = json.loads(node[0].decode())
        current_addrs.add("{}:{}".format(addr["host"], addr["port"]))

    G["servers"] = [RemoteServer(s) for s in current_addrs]


class RemoteServer:
    """封装rpc套接字对象"""
    def __init__(self, addr):
        self.addr = addr
        self._socket = None

    @property
    def socket(self):
        """惰性连接"""
        if not self._socket:
            self.connect()
        return self._socket

    def connect(self):
        """创建连接"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host, port = self.addr.split(":")
        sock.connect((host, int(port)))
        self._socket = sock

    def reconnect(self):
        """重连"""
        self.close()
        self.connect()

    def close(self):
        """关闭连接"""
        if self._socket:
            self._socket.close()
            self._socket = None

    def rpc(self, in_, params):
        """处理请求"""
        sock = self.socket
        request = json.dumps({"in": in_, "params": params})
        length_prefix = struct.pack("I", len(request))
        sock.send(length_prefix)
        sock.sendall(request.encode())
        length_prefix = sock.recv(4)
        length, = struct.unpack("I", length_prefix)
        body = sock.recv(length)
        response = json.loads(body.decode())
        return response["out"], response["result"]

    def ping(self, message):
        return self.rpc("ping", message)


if __name__ == '__main__':
    for i in range(100):
        server = random_server()
        if not server:
            break  # 如果没有节点存活，就退出
        time.sleep(1)
        try:
            out, result = server.ping("hello {}".format(i))
            print(server.addr, out, result)
        except Exception as ex:
            server.close()  # 遇到错误，关闭连接
            print(ex)

    time.sleep(1000)


























