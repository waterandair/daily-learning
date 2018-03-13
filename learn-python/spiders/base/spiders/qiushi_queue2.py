#!/usr/bin/python3
# -*- coding utf-8 -*-
import requests
from lxml import etree
import queue
import threading
import json
import time

class ThreadCrawl:
    def __init__(self):
        self._running = True
        self.thread_id = ''

    def run(self, thread_id, q):
        print("Starting threadCrawl", thread_id)
        self.thread_id = thread_id
        self.spider(q)
        print('Exiting threadCrawl', thread_id)

    def spider(self, q):
        while True:
            item = q.get()
            if item == _sentinel:
                """当返回为 _sentinel 时，终止线程，（队列中继续放入 _sentinel, 终止所有线程）"""
                q.put(_sentinel)
                break
            else:
                page = str(item)
                print('请求页面 线程 ——> {}  page ——> {}'.format(self.thread_id, page))
                fullurl = 'http://www.qiushibaike.com/8hr/page/' + str(page) + '/'
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
                    'Accept-Language': 'zh-CN,zh;q=0.8'
                }

                timeout = 4
                while timeout > 0:
                    try:
                        content = requests.get(fullurl, headers)
                        data_queue.put(content.text)
                        break
                    except Exception as e:
                        print('发送请求失败', e)
                        timeout -= 1

                if timeout <= 0:
                    print('timeout', fullurl)


class ThreadParser:
    """
    页面解析类
    """
    def __init__(self):
        pass

    def run(self, thread_id, locked, f):
        print('Starting threadParse', thread_id)
        global total
        while True:
            try:
                data = data_queue.get(block=False)
                if data == _sentinel:
                    data_queue.put(_sentinel)
                    break
                else:
                    self.parse(data, thread_id, locked, f)
                    data_queue.task_done()
                    print('解析完成', thread_id, total)
            except Exception as e:
                pass
        print('Exiting threadParse', thread_id)

    def parse(self, data, thread_id, locked, f):
        try:
            html = etree.HTML(data)
            lists = html.xpath('//div[contains(@id, "qiushi_tag")]')
            for li in lists:
                try:
                    imgurl = li.xpath('.//img/@src')
                    title = li.xpath('.//h2')[0].text
                    content = li.xpath('.//div[@class="content"]/span')[0]
                    content = li.xpath('string(.)')  # 提取一个标签下所有的内容
                    vote = None
                    comments = None
                    try:
                        vote = li.xpath('.//i')[0].text
                        comments = li.xpath('.//i')[1].text
                    except Exception as e:
                        pass

                    result = {
                        'imgUrl': imgurl,
                        'title': title,
                        'content': content,
                        'vote': vote,
                        'comments': comments,
                    }
                    with locked:
                        f.write(json.dumps(result, ensure_ascii=False) + "\n")
                except Exception as e:
                    print('解析失败或写入失败', thread_id, e)
                global total
                with locked:
                    total += 1

        except Exception as e:
            print('转为 html 失败', thread_id, e)


data_queue = queue.Queue()
_sentinel = object()
total = 0

if __name__ == '__main__':
    out_put = open('./qiushi_queue2.json', 'a')

    # 初始化爬取网页队列 （1-10 页）
    pageQueue = queue.Queue(50)
    for page in range(1, 11):
        pageQueue.put(page)
    pageQueue.put(_sentinel)

    # 初始化爬取线程
    crawlList = ["crawl-1", "crawl-2", "crawl-3"]
    crawlThreads = []
    for threadID in crawlList:
        crawl = ThreadCrawl()
        thread = threading.Thread(target=crawl.run, args=(threadID, pageQueue), name=threadID)
        thread.start()
        crawlThreads.append(thread)

    # 初始化解析线程
    parserThreads = []
    parserList = ["parser-1", "parser-2", "parser-3"]
    lock = threading.Lock()
    for threadID in parserList:
        parser = ThreadParser()
        thread = threading.Thread(target=parser.run, args=(threadID, lock, out_put), name=threadID)
        thread.start()
        parserThreads.append(thread)

    # data_queue.join()

    for crawlThread in crawlThreads:
        crawlThread.join()

    while not data_queue.empty():
        pass

    data_queue.put(_sentinel)

    for parserThread in parserThreads:
        parserThread.join()

    with lock:
        out_put.close()
        print('总数', total)

