#!/usr/bin/python3
# -*- coding utf-8 -*-
import requests
from lxml import etree
import queue
import threading
import time
import json


class ThreadCrawl(threading.Thread):
    """
    抓取线程类
    """
    def __init__(self, threadID, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.q = q

    def run(self):
        print("Starting " + self.threadID)
        self.qiushi_spider()
        print("Exiting" + self.threadID)

    def qiushi_spider(self):
        while True:
            if self.q.empty():
                break
            else:
                page = self.q.get()
                print('qiushi_spider={} page={}'.format(self.threadID, str(page)))
                url = 'http://www.qiushibaike.com/8hr/page/' + str(page) + '/'
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
                    'Accept-Language': 'zh-CN,zh;q=0.8'
                }

                # 多次尝试失败结束，防止死循环
                timeout = 4
            while timeout > 0:
                try:
                    content = requests.get(url, headers=headers)
                    data_queue.put(content.text)
                    break
                except Exception as e:
                    print('qiushi_spider', e)

            if timeout < 0:
                print('timeout', url)


class ThreadParser(threading.Thread):
    """
    页面解析类
    """
    def __init__(self, threadID, queue, lock, f):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.queue = queue
        self.lock = lock
        self.f = f

    def run(self):
        print('starting ', self.threadID)
        global total, exitFlag_Parser

        while not exitFlag_Parser:
            try:
                item = self.queue.get(False)
                if not item:
                    pass
                self.parse_data(item)
                self.queue.task_done()
                print('Thread_Parser=', self.threadID, 'total=', total)

            except Exception:
                pass

        print('Exiting', self.threadID)

    def parse_data(self, item):
        """
        解析网页函数
        :param item:
        :return:
        """
        global total
        try:
            html = etree.HTML(item)
            result = html.xpath('//div[contains(@id, "qiushi_tag")]')
            for site in result:
                try:
                    imgurl = site.xpath('.//img/@src')
                    title = site.xpath('.//h2')[0].text
                    content = site.xpath('.//div[@class="content"]/span')[0]
                    content = content.xpath('string(.)')  # 提取一个标签下所有的内容
                    vote = None
                    comments = None
                    try:
                        vote = site.xpath('.//i')[0].text
                        comments = site.xpath('.//i')[1].text
                    except Exception as e:
                        pass

                    result = {
                        'imgUrl': imgurl,
                        'title': title,
                        'content': content,
                        'vote': vote,
                        'comments': comments,
                    }
                    with self.lock:
                        # print 'write %s' % json.dumps(result)
                        self.f.write(json.dumps(result, ensure_ascii=False) + "\n")
                except Exception as e:
                    print('site in result', e)
        except Exception as e:
            print('parse_data', e)
        with self.lock:
            total +=1


data_queue = queue.Queue()
exitFlag_Parser = False
lock = threading.Lock()
total = 0

if __name__ == '__main__':
    out_put = open('./qiushi_queue.json', 'a')

    # 初始化网页也发从1-10个页面
    pageQueue = queue.Queue(50)
    for page in range(1, 11):
        pageQueue.put(page)

    # 初始化采集线程
    crawlthreads = []
    crawlList = ["crawl-1", "crawl-2", "crawl-3_num_date_time"]

    for threadID in crawlList:
        thread = ThreadCrawl(threadID, pageQueue)
        thread.start()
        crawlthreads.append(thread)

    # 初始化解析线程
    parserThreads = []
    parserList = ["parser-1", "parser-2", "parser-3_num_date_time"]
    # 分别启动
    for threadID in parserList:
        thread = ThreadParser(threadID, data_queue, lock, out_put)
        thread.start()
        parserThreads.append(thread)

    # 等待队列清空
    while not pageQueue.empty():
        pass

    for t in crawlthreads:
        t.join()

    while not data_queue.empty():
        pass

    # 通知线程是时候退出了
    global exitFlag_Parser
    exitFlag_Parser = True

    for t in parserThreads:
        t.join()
    print("exiting main thread")

    with lock:
        out_put.close()