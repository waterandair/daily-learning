#!/usr/bin/ python3
# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):

    CSRF_ENABLED = True
    # 每页显示数量
    POSTS_PER_PAGE = 3
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:000000@127.0.0.1:3306/flask_demo?charset=utf8mb4'
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #SQLALCHEMY_ECHO = True

    """邮件相关的配置 测试服务器：python -m smtpd -n -c DebuggingServer localhost:8025 """
    MAIL_SERVER = "smtp.qq.com"
    MAIL_PORT = 465
    MAIL_USE_TLS = 0
    MAIL_USE_SSL = 1
    MAIL_USERNAME = "156577812@qq.com"
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['156577812@qq.com']


