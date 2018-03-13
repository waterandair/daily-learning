#!/usr/bin/python3
# -*- coding utf-8 -*-
from http import cookiejar
from urllib import request
from urllib import parse

# 构建一个 CookieJar 对象实例保存 cookie
cj = cookiejar.CookieJar()
# 使用 HTTPCookieProcessor() 创建 Cookie 处理器对象
handler = request.HTTPCookieProcessor(cj)
# 通过 build_opener() 来构建 opener()
opener = request.build_opener(handler)
# addheaders 接受一个 tuple 列表 ，可以添加header信息
opener.addheaders = [("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36")]

# 登录账号
data = {
    'account_name': '15210014736',
    'user_pwd': 'zhangji123',
    'remember_me': 'N'
}
# 通过 parse.urlencode 转码
postData = parse.urlencode(data).encode("utf-8")

# 构建 Request 请求对象，包含需要发送的用户名和密码
req = request.Request("https://www.mosoteach.cn/web/index.php?c=passport&m=account_login", data=postData)
opener.open(req)

# opener 包含用户登录后的 Cookie 值，可以直接访问登录或才可以访问的页面
response = opener.open("https://www.mosoteach.cn/web/index.php?c=clazzcourse&m=index")
print(response.read().decode('utf-8'))