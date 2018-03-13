# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy import Request, FormRequest
from mySpider.items import MosoteachItem


class MosoteachSpider(CrawlSpider):
    name = 'mosoteach'
    allowed_domains = ['mosoteach.cn']
    start_urls = [
        'https://www.mosoteach.cn/web/index.php?c=clazzcourse&m=index'
    ]

    rules = (
        Rule(LinkExtractor(allow=r"[a-zA-z]+://www.mosoteach.cn/web/index.php\?c=interaction&m=index[.]*", attrs=['data-url']), callback='parse_page'),
    )

    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip,deflate",
        "Accept-Language": "en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4",
        "Connection": "keep-alive",
        "Content-Type": " application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
        "Referer": "https://www.mosoteach.cn/"
    }
    meta = {'cookiejar': 1}

    # 重写了爬虫类的方法，实现了自定义请求，运行成功后会
    def start_requests(self):
        print("Preparing login")
        url = 'https://www.mosoteach.cn/web/index.php?c=passport&m=account_login'
        ajax = {'X-Requested-With': 'XMLHttpRequest'}
        headers = self.headers.update(ajax)
        formdata = {
            'account_name': '15210014736',
            'user_pwd': 'pwd123456',
            'remember': 'N'
        }
        return [
            FormRequest(url=url, meta=self.meta, formdata=formdata, headers=headers, callback=self.after_login)
        ]

    def after_login(self, response):
        print(response.headers.getlist('Set-Cookie'))
        self.headers.pop('X-Requested-With')
        for url in self.start_urls:
            yield Request(url, dont_filter=True, meta=self.meta)

    def parse_page(self, response):
        print("**********************************")
        print(response.request.headers)
        print(response.url)
        title = response.xpath('//title').extract()
        print(title)
        return title
