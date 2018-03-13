#!/usr/bin/python3
# coding utf-8
import ipaddress
"""
You have a CIDR network address such as "123.45.67.89/27" , and you want to generate a range of all the IP address that
it represents
The ipaddress module can be easily used to perform such calculations.
"""
net = ipaddress.ip_network('123.45.67.64/27')
for ip in net:
    print(ip)

a = ipaddress.ip_address('123.45.67.69')
print(a in net)  # True
b = ipaddress.ip_address('123.45.67.123')
print(b in net)  # False


"""
An IP address and network address can be specified together as an IP interface
"""
inet = ipaddress.ip_interface('123.45.67.73/27')
print(inet.network)  # 123.45.67.64/27
print(inet.ip)  # 123.45.67.73