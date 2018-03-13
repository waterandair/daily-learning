#!/usr/bin/python3
# coding utf-8
from urllib import request
from urllib import parse
import urllib


def load_page(fullurl, filename):
    print('正在下载' + filename)

    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;'
    }
    req = request.Request(fullurl, headers=headers)
    res = request.urlopen(req)
    return res.read()


def write_file(html, filename):
    print("正在存储" + filename)
    with open('./data/' + filename, 'wt') as f:
        f.write(html.decode('utf-8'))
    print("*" * 20)


def tieba_spider(url, beginPage, endPage):
    """
    deal with url, send a request to each url
    :param url:
    :param beginPage:
    :param endPage:
    :return:
    """
    for page in range(beginPage, endPage+1):
        pn = (page - 1) * 50
        fullurl = url + "&pn=" + str(pn)
        filename = "page_{}.html".format(str(page))

        html = load_page(fullurl, filename)
        write_file(html, filename)







if __name__ == '__main__':
    kw = input("请输入需要爬取的贴吧:")
    beginPage = int(input('请输入起始页:'))
    endPage = int(input('请输入终止页:'))

    url = "http://tieba.baidu.com/f?"
    key = parse.urlencode({'kw': kw})
    url = url + key

    tieba_spider(url, beginPage, endPage)

