# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MyspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ItcastItem(scrapy.Item):
    name = scrapy.Field()
    level = scrapy.Field()
    info = scrapy.Field()


class MosoteachItem(scrapy.Item):
    class_name = scrapy.Field()
    act_name = scrapy.Field()
    act_status = scrapy.Field()
    act_ctime = scrapy.Field()
    act_join_status = scrapy.Field()


class DouyuItem(scrapy.Item):
    name = scrapy.Field()
    imagesUrls = scrapy.Field()
    imagesPath = scrapy.Field()


class SinaItem(scrapy.Item):
    # 大类的标题和 url
    parent_title = scrapy.Field()
    parent_urls = scrapy.Field()

    # 小类的标题和 子 url
    sub_title = scrapy.Field()
    sub_urls = scrapy.Field()

    # 小类目录存储路径
    sub_filename = scrapy.Field()

    # 小类下的子链接
    son_urls = scrapy.Field()

    # 文章的标题和内容
    head = scrapy.Field()
    content = scrapy.Field()

