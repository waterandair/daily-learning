#!/usr/bin/python3
# -*- coding utf-8 -*-
from urllib import request

# 构建 Request 请求
req = request.Request("https://www.baidu.com")

# 构建一个 HttpHandler 处理器对象，支持处理 HTTP 对象  (HTTPS 对象 request.HTTPSHandler())
http_handler = request.HTTPSHandler(debuglevel=1)  # 开启Debug Log，debuglevel 默认为1
# 创建支持处理 HTTP 请求的 opener 对象
opener = request.build_opener(http_handler)

# 调用自定义的 opener 对象 的 open() 方法，发送 request 请求
response = opener.open(req)

print(response.read())
