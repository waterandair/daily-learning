#!/usr/bin/python3
# -*- coding utf-8 -*-
import tornado.web
import tornado.ioloop
import tornado.httpserver


class IndexHandler(tornado.web.RequestHandler):
    """主路由处理类"""
    def get(self, *args, **kwargs):
        """对应 http 的 get 请求方式"""
        self.write("hello world")


if __name__ == '__main__':
    app = tornado.web.Application([
        (r"/", IndexHandler)
    ])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(81)
    # app.listen(81)  # 简写
    # IOLoop.current() 返回当前线程的IOLoop实例。 IOLoop.start() 启动IOLoop实例的I/O循环,同时服务器监听被打开。
    tornado.ioloop.IOLoop.current().start()

