#!/usr/bin/python3
# -*- coding utf-8 -*-
from urllib import request
from http import cookiejar

# 构建一个 CookieJar 对象实例来保存cookie
cj = cookiejar.CookieJar()

# 使用 HTTPCookieProcessor() 来创建 cookie 处理器对象，参数为 CookieJar() 对象
handler = request.HTTPCookieProcessor(cj)
# 通过 build_opener() 来构建 opener
opener = request.build_opener(handler)
# 以 get 方法访问页面，访问之后会自动保存 cookie 到 cookiejar 中
opener.open("http://www.baidu.com")

# 按标准格式将保存的 cookie 打印出来、
cookieStr = ''.join([item.name + '=' + item.value + ';' for item in cj])

# 舍去最后一个分号
print(cookieStr[:-1])
