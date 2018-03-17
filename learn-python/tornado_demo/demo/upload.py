#!/usr/bin/python3
# -*- coding utf-8 -*-

import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
from tornado.options import options, define
from tornado.web import RequestHandler

define("port", default=81, type=int, help="运行的端口")


class IndexHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.write("hello")


class UploadHandler(RequestHandler):
    def post(self, *args, **kwargs):
        files = self.request.files
        img_files = files.get('img')
        self.write("123")
        if img_files:
            img_files = img_files[0]["body"]
            with open("./file.png", 'wb') as f:
                f.write(img_files)

        self.write("ok")


if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application([
        (r"/", IndexHandler),
        (r"/upload", UploadHandler)
    ])

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()