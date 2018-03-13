#!/usr/bin/python3
# -*- coding utf-8 -*-
import urllib.request
import re

class Spider:

    def load_page(self, page):
        url = "http://www.neihan8.com/article/list_5_" + str(page) + ".html"
        user_agent = 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT6.1; Trident/5.0'
        headers = headers = {'User-Agent': user_agent}

        req = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req)
        html = response.read().decode('gbk')

        pattern = re.compile(r'<div.*?class="f18 mb20">(.*?)</div>', re.S)
        item_list = pattern.findall(html)
        return item_list

    def printOnePage(self, item_list, page):
        """
        :param item_list:
        :param page:
        :return:
        """
        print("******第{}页 爬取完毕...******".format(page))
        for item in item_list:
            print("==============")
            item = item.replace("<p>", "").replace("</p>", "").replace("<br />", "")
            print(item)

if __name__ == '__main__':
    print("按下回车键")
    input()
    mySpider = Spider()
    mySpider.printOnePage(mySpider.load_page(1), 1)