#!/usr/bin/python3
# -*- coding utf-8 -*-
import os
list = os.popen('nmap -sP 172.16.1.0/24')
print(list.read())