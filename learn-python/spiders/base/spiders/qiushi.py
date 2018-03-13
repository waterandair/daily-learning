#!/usr/bin/python3
# coding utf-8
import requests
from lxml import etree
import sys

page = 1
url = 'http://www.qiushibaike.com/8hr/page/' + str(page)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
    'Accept-Language': 'zh-CN,zh;q=0.8'
}

response = requests.get(url, headers=headers).text
html = etree.HTML(response)
html = html.xpath('//div[contains(@id, "qiushi_tag")]')

for site in html:
    item = {}
    imgUrl = site.xpath('./div/a/img/@src')
    username = site.xpath('.//h2')[0].text
    content = site.xpath('.//div[@class="content"]/span')[0]
    content = content.xpath('string(.)')  # 提取一个标签下所有的内容
    # 投票次数
    vote = site.xpath('.//i')[0].text
    # print site.xpath('.//*[@class="number"]')[0].text
    # 评论信息
    comments = site.xpath('.//i')[1].text

    print(imgUrl, username, content, vote, comments)
