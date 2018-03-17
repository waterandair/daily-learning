#!/usr/bin/python3
# -*- coding utf-8 -*-
import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
from tornado.web import url, RequestHandler
import config

tornado.options.define('port', default=81, type=int, help="服务运行的端口")
tornado.options.define('multiple', default=[], multiple=True, help="一个变量多个值")


class IndexHandler(RequestHandler):
    """主路由处理类"""
    def get(self, *args, **kwargs):
        """对应 http get 请求"""
        python_url = self.reverse_url("python_url")
        self.write("<a href='" + python_url +"'>python</a>")


class SubjectHandler(RequestHandler):

    def initialize(self, subject):
        self.subject = subject

    def get(self, *args, **kwargs):
        self.write(self.subject)


if __name__ == '__main__':
    tornado.options.parse_command_line()  # 这里也可以用读取文件的方式 tornado.options.parse_config_file("./config")
    # 调用 parse_command_line() 和 parse_config_file("./config") 默认会配置标准logging 模块, 如果想关闭,
    # 可以在命令行中加入 --logging=none 或 代码中设置
    tornado.options.logging = None
    print(tornado.options.options.multiple)
    app = tornado.web.Application([
        (r"/", IndexHandler),
        (r"/java", SubjectHandler, {'subject': 'java'}),
        # name是给该路由起一个名字，可以通过调用RequestHandler.reverse_url(name)来获取该名子对应的url。
        url(r"/python", SubjectHandler, {'subject': 'python'}, name='python_url')
    ],
        **config.settings,  # 导入配置文件
    )
    print(config.redis_options['redis_host'])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(tornado.options.options.port)
    tornado.ioloop.IOLoop.current().start()

    # 执行 python3 opt.py --port=82 --multiple=a,b,c

