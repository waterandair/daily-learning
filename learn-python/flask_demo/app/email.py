#!/usr/bin/ python3
# -*- coding: utf-8 -*-
from flask import render_template
from flask_mail import Message
from app import app, mail
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
    Thread(target=send_async_email, args=(app, msg)).start()


def send_async_email(app, msg):
    """
    异步发送邮件
    :param app:
    :param msg:
    :return:
    """
    with app.app_context():
        mail.send(msg)


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('flask-demo 重置密码', sender=app.config['ADMINS'][0], recipients=[user.email],
               text_body=render_template('email/reset_password.txt', user=user, token=token),
               html_body=render_template('email/reset_password.html', user=user, token=token))