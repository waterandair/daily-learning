# -*- coding: utf-8 -*-
import scrapy
from mySpider.items import ItcastItem


class ItcastSpider(scrapy.Spider):
    name = 'itcast'
    allowed_domains = ['itcast.cn']
    start_urls = ['http://www.itcast.cn/channel/teacher.shtml']

    def parse(self, response):
        items = []
        for data in response.xpath("//div[@class='li_txt']"):
            # 将得到的数据封装到一个 ‘ItcastItem’ 对象
            item = ItcastItem()

            # extract() 方法返回的都是 unicode 字符串
            item['name'] = data.xpath("h3/text()").extract()[0]
            item['level'] = data.xpath("h4/text()").extract()[0]
            item['info'] = data.xpath("p/text()").extract()[0]

            items.append(item)
            yield item





