#!/usr/bin/python3
# -*- coding utf-8 -*-
import os
# Redis配置
redis_options = {
    'redis_host':'127.0.0.1',
    'redis_port':6379,
    'redis_pass':'',
}

# Tornado app配置
settings = {
    'template_path': os.path.join(os.path.dirname(__file__), 'templates'),
    'static_path': os.path.join(os.path.dirname(__file__), 'statics'),
    'cookie_secret':'0Q1AKOKTQHqaa+N80XhYW7KCGskOUE2snCW06UIxXgI=',
    'xsrf_cookies': False,
    'login_url': '/login',
    'debug': True,
    # 调试模式:
    # 自动重启
    # 取消缓存编译的模板，可以单独通过compiled_template_cache=False来设置；
    # 取消缓存静态文件hash值，可以单独通过static_hash_cache=False来设置；
    # 提供追踪信息，当RequestHandler或者其子类抛出一个异常而未被捕获后，会生成一个包含追踪信息的页面，可以单独通过serve_traceback=True来设置。
}

# 日志
log_path = os.path.join(os.path.dirname(__file__), 'logs/log')
