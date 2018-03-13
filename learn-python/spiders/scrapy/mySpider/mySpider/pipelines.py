# -*- coding: utf-8 -*-
import scrapy
import os
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.project import get_project_settings
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

class MyspiderPipeline(object):
    def process_item(self, item, spider):
        content = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(content)
        return item


class ImagesPipeline(ImagesPipeline):
    IMAGES_STORE = get_project_settings().get('IMAGES_STORE')

    def get_media_requests(self, item, info):
        image_url = item['imagesUrls']
        yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        image_path = [x['path'] for ok, x in results if ok]
        name, ext = os.path.splitext(image_path[0])
        os.rename(self.IMAGES_STORE + '/' + image_path[0], self.IMAGES_STORE + '/' + item['name'] + ext)
        item["imagesPath"] = self.IMAGES_STORE + '/' + item['name']

        return item

class SinaPipeline(object):
    def process_item(self, item, spider):
        son_urls = item['son_urls']

        # 文件名为head
        with open(item['sub_filename'] + '/' + item['head'] + '.txt', 'w') as f:
            f.write(item['content'])

        return item
