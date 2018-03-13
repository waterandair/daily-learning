# -*- coding: utf-8 -*-
import scrapy
import os
from mySpider.items import SinaItem


class SinaSpider(scrapy.Spider):
    name = 'sina'
    allowed_domains = ['sina.com.cn']
    start_urls = ['http://news.sina.com.cn/guide/']

    def parse(self, response):
        items = []
        # 所有大类的url和标题
        parent_url = response.xpath('//h3[@class="tit02"]/a/@href').extract()
        parent_title = response.xpath('//h3[@class="tit02"]/a/text()').extract()

        sub_urls = response.xpath('//ul[@class="list01"]/li/a/@href').extract()
        sub_title = response.xpath('//ul[@class="list01"]/li/a/text()').extract()

        parent_len = len(parent_url)
        for i in range(0, parent_len):
            # 指定大类目录的路径和目录名
            parent_filename = "./sina/" + parent_title[i]

            # 如果目录不存在，则创建目录
            if not os.path.exists(parent_filename):
                os.makedirs(parent_filename)

            # 爬取所有小类
            sub_len = len(sub_urls)
            for j in range(0 , sub_len):
                item = SinaItem()

                # 保存大类的title和urls
                item['parent_title'] = parent_title[i]
                item['parent_urls'] = parent_url[i]

                if_belong = sub_urls[j].startswith(item['parent_urls'])

                if(if_belong):
                    sub_filename = parent_filename + '/' + sub_title[j]
                    # 如果目录不存在，则创建目录
                    if not os.path.exists(sub_filename):
                        os.makedirs(sub_filename)

                    # 存储 小类 title 和 urls 和 filenames
                    item['sub_title'] = sub_title[j]
                    item['sub_urls'] = sub_urls[j]
                    item['sub_filename'] = sub_filename

                    items.append(item)

        for item in items:
            yield scrapy.Request(url=item['sub_urls'], meta={'meta_1': item}, callback=self.second_parse)

    def second_parse(self, response):
        # 提取每次 Response 的数据
        meta_1 = response.meta['meta_1']

        # 取出小类中所有的文章链接
        son_urls = response.xpath('//a/@href').extract()
        son_urls_len = len(son_urls)
        # 取出小类中所有子链接
        items = []

        for i in range(0, son_urls_len):
            # 过滤掉无用的url
            if_belong =  son_urls[i].endswith('.shtml') and son_urls[i].startswith(meta_1['parent_urls'])

            if if_belong:
                item = SinaItem()
                item['parent_title'] = meta_1['parent_title']
                item['parent_urls'] = meta_1['parent_urls']
                item['sub_urls'] = meta_1['sub_urls']
                item['sub_title'] = meta_1['sub_title']
                item['sub_filename'] = meta_1['sub_filename']
                item['son_urls'] = son_urls[i]
                items.append(item)

        for item in items:
            yield scrapy.Request(url=item['son_urls'], meta={'meta_2': item}, callback=self.parse_detail)

    def parse_detail(self, response):
        item = response.meta['meta_2']
        content = ''
        head = ''
        head1 = response.xpath('//h1[@id="main_title"]/text()').extract()
        head2 = response.xpath('//h1[@id="artibodyTitle"]/text()').extract()
        if head1:
            head = head1[0]
        elif head2:
            head = head2[0]
        else:
            head = item['son_urls'][-20:-6]
        content_list = response.xpath('//div[@id="artibody"]/p/text()').extract()

        # 将p标签里的内容合并到一起
        for c in content_list:
            content += c + "\n"

        item['head'] = head
        item['content'] = content

        yield item



