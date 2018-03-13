# -*- coding: utf-8 -*-
import scrapy
from mySpider.items import TencentItem
import re


class TencentSpider(scrapy.Spider):
    name = 'tencent'
    allowed_domains = ['hr.tencent.com']
    start_urls = ['http://hr.tencent.com/position.php?&start=0#a']

    def parse(self, response):
        for data in response.xpath('//*[@class="even"]'):
            item = TencentItem()
            name = data.xpath('./td[1]/a/text()').extract()[0]
            detailLink = data.xpath('./td[1]/a/@href').extract()[0]
            positionInfo = data.xpath('./td[2]/text()').extract()[0]
            peopleNumber = data.xpath('./td[3]/text()').extract()[0]
            workLocation = data.xpath('./td[4]/text()').extract()[0]
            publishTime = data.xpath('./td[5]/text()').extract()[0]

            item['name'] = name
            item['detailLink'] = detailLink
            item['positionInfo'] = positionInfo
            item['peopleNumber'] = peopleNumber
            item['workLocation'] = workLocation
            item['publishTime'] = publishTime

            curpage = re.search('(\d+)', response.url).group(1)
            page = int(curpage) + 10
            url = re.sub('\d+', str(page), response.url)

            # 发送新的url请求加入待爬队列，并调用回调函数 self.parse
            yield scrapy.Request(url, callback=self.parse)

            # 将获取的数据交给pipeline
            yield item
