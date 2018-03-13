#!/usr/bin/python3
# -*- coding utf-8 -*-
import requests

"""get 请求"""
response = requests.get("http://www.baidu.com")
print(response)  # <Response [200]>

kw = {'wd': 'nba'}
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
response = requests.get("http://www.baidu.com/s?", params=kw, headers=headers)

# print(response)  # <Response [200]>
# print(response.text)  # 查看响应内容， 返回 unicode 格式的数据
# print(response.content)  # 查看响应内容， 返回字节流数据
# print(response.url)  # 查看完整 url 地址   http://www.baidu.com/s?wd=nba
# print(response.encoding)  # 查看响应头部字符编码  utf-8
# print(response.status_code)  # 查看响应码  200


"""post 请求"""
formdata = {
    "type": "AUTO",
    "i": "i love python",
    "doctype": "json",
    "xmlVersion": "1.8",
    "keyfrom": "fanyi.web",
    "ue": "UTF-8",
    "action": "FY_BY_ENTER",
    "typoResult": "true"
}
url = "http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=null"

response = requests.post(url, data=formdata, headers=headers)
print(response.text)
print(type(response.json()))

