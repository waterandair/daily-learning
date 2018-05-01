#!/usr/bin/ python3
# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from app.models import User


class EditProfileForm(FlaskForm):
    """
    编辑用户信息
    """
    username = StringField('用户名：', validators=[DataRequired()])
    about_me = TextAreaField('关于我：', validators=[Length(min=0, max=140)])
    submit = SubmitField("提交")

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError("该用户名已被占用")


class PostForm(FlaskForm):
    """
    写文章
    """
    post = TextAreaField('写一写', validators=[DataRequired(), Length(min=1, max=140)])
    submit = SubmitField('提交')
