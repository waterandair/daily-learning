#!/usr/bin/python3
# -*- coding utf-8 -*-
from urllib import request
from http import cookiejar

filename = 'cookie.txt'

# 声明一个 MozillaCookieJar 对象实例保存 cookie ，之后写入文件
cj = cookiejar.MozillaCookieJar(filename)

# 使用 HTTPCookieProcessor() 来创建 Cookie 处理器对象，参数为 CookieJar 对象
handler = request.HTTPCookieProcessor(cj)

# 使用 build_opener() 来构建 opener
opener = request.build_opener(handler)
response = opener.open("http://www.baidu.com")

cj.save()