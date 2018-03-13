#!/usr/bin/python3
# -*- coding utf-8 -*-
from http import cookiejar
from urllib import request

# 创建 MozillaCookieJar 实例对象
cj = cookiejar.MozillaCookieJar()
# 从文件中读取 cookie 内容到变量
cj.load('cookie.txt')
# 使用 HTTPCookieProcessor() 来创建 cookie 处理器对象
handler = request.HTTPCookieProcessor(cj)
# 使用 build_opener() 构建 opener
opener = request.build_opener(handler)

response = opener.open("http://www.baidu.com")
print(response.read().decode('utf-8'))
