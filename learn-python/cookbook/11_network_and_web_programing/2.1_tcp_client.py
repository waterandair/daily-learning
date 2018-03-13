#!/usr/bin/python3
# coding utf-8
from socket import socket, AF_INET, SOCK_STREAM

s = socket(AF_INET, SOCK_STREAM)
s.connect(('127.0.0.1', 2000))
# s.send(b'hello')
# print(s.recv(1024))