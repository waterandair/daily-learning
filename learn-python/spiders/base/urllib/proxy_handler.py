#!/usr/bin/python3
# coding utf-8
from urllib import request

# 构建两个代理 Handler
http_proxy_handler = request.ProxyHandler({"http": "119.36.92.47:80"})
null_proxy_handler = request.ProxyHandler({})
# 定义一个代理开关
proxySwitch = True

if proxySwitch:
    opener = request.build_opener(http_proxy_handler)
else:
    opener = request.build_opener(null_proxy_handler)

req = request.Request("http://www.baidu.com")

# 这种写法，只有使用 opener.open() 方法发送请求才使用自定义的代理， 而 urlopen() 则不使用自定义代理
response = opener.open(req, timeout=60)

# 这种写法，就是将 opener 应用到全局， 之后用 opener.open() 和 urlopen() 发送的请求，都将使用自定义代理
request.install_opener(opener)
response = request.urlopen(req)

print(response.read().decode('gbk', errors='ignore'))