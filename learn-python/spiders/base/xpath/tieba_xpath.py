#!/usr/bin/python3
# coding UTF-8

import os
from urllib import request
from urllib import parse
from lxml import etree
import re

class Spider:
    def __init__(self):
        self.tiebaName = input('请输入要访问的贴吧: ')
        self.beginPage = int(input('请输入起始页: '))
        self.endPage = int(input('请输入终止页: '))

        self.url = 'http://tieba.baidu.com/f'
        self.ua_header = {"User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1 Trident/5.0;"}

        # 图片编号
        self.userName = 1

    def tieba_spider(self):
        for page in range(self.beginPage, self.endPage + 1):
            pn = (page - 1) * 50
            word = {"pn":pn, "kw":self.tiebaName}

            word = parse.urlencode(word)
            fullUrl = self.url + "?" + word
            self.load_page(fullUrl)

    def load_page(self, url):
        req = request.Request(url, headers=self.ua_header)
        html = request.urlopen(req).read()

        # 解析 html 为 HTML 文档
        selector = etree.HTML(html)
        tieziLinks = selector.xpath('//div[@class="threadlist_lz clearfix"]/div/a/@href')

        for link in tieziLinks:
            link = "http://tieba.baidu.com" + link
            self.load_images(link)

    def load_images(self, link):
        req = request.Request(link, headers=self.ua_header)
        html = request.urlopen(req).read()

        selector = etree.HTML(html)
        imagesLinks = selector.xpath('//img[@class="BDE_Image"]/@src')

        # 取出图片,下载保存
        for link in imagesLinks:
            self.downloadImage(link)

    def downloadImage(self, link):
        print(link)
        print('正在存储文件 ' + str(self.userName))

        name, ext = os.path.splitext(link)
        # ext = re.findall(r'\.[^.\\/:*?"<>|\r\n]+$', link).pop()
        # 打开文件,返回一个文件对象
        with open('./images/' + str(self.userName) + ext, 'wb') as f:
            image = request.urlopen(link).read()
            f.write(image)
        self.userName += 1


if __name__ == '__main__':
    spider = Spider()
    spider.tieba_spider()