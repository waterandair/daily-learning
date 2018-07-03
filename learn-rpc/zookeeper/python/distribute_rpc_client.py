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
    """
    随机获取一个服务节点
    :return:
    """


def get_servers():
    zk = KazooClient(hosts="127.0.0.1:2181")
    zk.start()
    # 当前活跃地址列表
    current_addrs = set()

    def watch_servers(*args):
        """
        监听服务器地址
        :param args:
        :return:
        """
        new_addrs = set()
        # 获取新的服务地址列表,并支持监听服务列表变动
        for child in zk.get_children(zk_root, watch=watch_servers):
            node = zk.get(zk_root + "/" + child)
            addr = json.loads(node[0])
            new_addrs.add("{}:{}".format(addr["host"], addr["port"]))

        # 删除的地址, 删除对应地址的server
        del_addrs = current_addrs - new_addrs
        del_servers = []

        # 找出所有待删除的 server 对象
        for addr in del_addrs:
            for s in G["servers"]:
                if s.addr == addr:
                    del_servers.append(s)
                    break

        # 删除待删除的server
        for server in del_servers:
            G["servers"].remove(server)
            current_addrs.remove(server.addr)

        # 新增的地址
        add_addrs = new_addrs - current_addrs
        # 新增server
        for addr in add_addrs:
            G["servers"].append(RemoteServer(addr))
            current_addrs.add(addr)


class RemoteServer():
    def __init__(self, addr):
        pass


if __name__ == '__main__':
    for i in range(100):
        server = random_server()

























