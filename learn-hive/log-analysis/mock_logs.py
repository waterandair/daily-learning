#!/usr/bin/ python3
# -*- coding: utf-8 -*-
import random
import struct
import socket
import time
import os
RANDOM_IP_POOL = ['192.168.10.222/0']


def generate_ip():
    str_ip = RANDOM_IP_POOL[random.randint(0, len(RANDOM_IP_POOL) - 1)]
    str_ip_addr = str_ip.split('/')[0]
    str_ip_mask = str_ip.split('/')[1]
    ip_addr = struct.unpack('>I', socket.inet_aton(str_ip_addr))[0]
    mask = 0x0
    for i in range(31, 31 - int(str_ip_mask), -1):
        mask = mask | (1 << i)
    ip_addr_min = ip_addr & (mask & 0xffffffff)
    ip_addr_max = ip_addr | (~mask & 0xffffffff)
    return socket.inet_ntoa(struct.pack('>I', random.randint(ip_addr_min, ip_addr_max)))


def generate_time(start=2017, end=2018):
    start = time.mktime((start, 1, 1, 0, 0, 0, 0, 0, 0))
    end = time.mktime((end, 1, 1, 0, 0, 0, 0, 0, 0))
    timestamp = random.randint(start, end)
    # 21/Nov/2017:20:35:03 +0800
    datetime = time.strftime("%d/%b/%Y:%H:%M:%S", time.localtime(timestamp))
    return datetime


def generate_request():
    method = random.choice(['GET', 'POST'])
    if method == 'GET':
        page = random.choice(['/login', '/index', '/news', '/profile', '/learn/1', '/learn/2', '/learn/3'])
    else:
        page = random.choice(['/login', '/logout', '/profile/edit'])
    return "{} {} HTTP/1.1".format(method, page)


def generate_user_agent():
    return random.choice([
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
        "User-Agent:Mozilla/5.0(Macintosh;U;IntelMacOSX10_6_8;en-us)AppleWebKit/534.50(KHTML,likeGecko)Version/5.1Safari/534.50",
        "User-Agent:Mozilla/5.0(compatible;MSIE9.0;WindowsNT6.1;Trident/5.0;",
        "Mozilla/5.0 (Linux; U; Android 2.0; en-us; Droid Build/ESD20) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17 "
        ]
    )


def generate_status():
    seq = [200 for i in range(100)]
    seq.append(404)
    seq.append(500)
    seq.append(302)
    return random.choice(seq)


def generate_body_length():
    return random.choice(range(1000))


def mock_access_log(nums=10000):
    path = os.path.dirname(os.path.realpath(__file__))

    while nums > 0:
        nums -= 1
        line = '"{}" "{}" "{}" "{}" "{}" "{}"'.format(
            generate_ip(),
            generate_time(),
            generate_request(),
            generate_status(),
            generate_body_length(),
            generate_user_agent()
        )
        with open(path + "/access.log", 'a') as f:
            f.write(line + "\n")


if __name__ == '__main__':
    mock_access_log()
