# -*- coding: utf-8 -*-
import scrapy
import json
from mySpider.items import DouyuItem


class DouyuSpider(scrapy.Spider):
    name = 'douyu'
    allowed_domains = ['capi.douyucdn.cn']

    offset = 0
    url = 'http://capi.douyucdn.cn/api/v1/getVerticalRoom?limit=20&offset='
    start_urls = [
        url + str(offset)
    ]

    def parse(self, response):
        # 返回从 json 里获取 data 段数据集合
        data = json.loads(response.text)['data']

        for i in data:
            item = DouyuItem()
            item['name'] = i['nickname']
            item['imagesUrls'] = i['vertical_src']

            yield item

        self.offset += 20
        yield scrapy.Request(self.url + str(self.offset), callback=self.parse)
