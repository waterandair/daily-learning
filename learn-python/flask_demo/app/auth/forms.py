#!/usr/bin/ python3
# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from app.models import User


class LoginForm(FlaskForm):
    """
    登录
    """
    username = StringField('姓名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('记住我', default=False)
    submit = SubmitField('登录')


class RegistrationFrom(FlaskForm):
    """
    注册
    """
    username = StringField('用户名', validators=[DataRequired("用户名不能为空")])
    email = StringField('邮箱', validators=[DataRequired('邮箱不能为空'), Email("请输入正确的邮箱")])
    password = PasswordField('密码', validators=[DataRequired()])
    password2 = PasswordField('再次输入', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('注册')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("用户名已被注册，请更换重试")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("邮箱已被注册， 请更换成功重试")


class ResetPasswordRequestForm(FlaskForm):
    """
    请求重置密码
    """
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    submit = SubmitField('重置密码')


class ResetPasswordForm(FlaskForm):
    """
    重置密码
    """
    password = PasswordField('密码', validators=[DataRequired()])
    password2 = PasswordField('重复密码', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('重置')



