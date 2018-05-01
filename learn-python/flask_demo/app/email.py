#!/usr/bin/ python3
# -*- coding: utf-8 -*-
from flask_mail import Message
from flask import current_app
from app import mail
from threading import Thread


def send_email(subject, sender, recipients, text_body, html_body):
    """
    发送邮件
    :param subject:
    :param sender:
    :param recipients:
    :param text_body:
    :param html_body:
    :return:
    """
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    # current_app 是一个和请求上下文相关的变量.在不同的线程中, current_app 没有赋值， current_app 是应用对象的动态代理
    Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()


def send_async_email(app, msg):
    """
    异步发送邮件
    :param app:
    :param msg:
    :return:
    """
    with app.app_context():
        mail.send(msg)