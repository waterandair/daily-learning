#!/usr/bin/python3
# coding utf8
from urllib import request
response = request.urlopen('http://www.baidu.com')
html = response.read()

req = request.Request('http://www.baidu.com', data=b'', headers={})
response = request.urlopen(req)
html = response.read()

print(html)
