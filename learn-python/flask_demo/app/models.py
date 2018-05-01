#!/usr/bin/ python3
# -*- coding: utf-8 -*-
from datetime import datetime
from time import time
import jwt
from hashlib import md5
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login
from flask import current_app


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


# 辅助表不需要创建一个类， 两个字段都是 user 的外键
followers = db.Table('followers',
                     db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
                     db.Column('followed_id', db.Integer, db.ForeignKey('user.id')),
                     )


class User(UserMixin, db.Model):
    """
    用户模型
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    # 一对多关联到 Post 模型. 这是一层抽象，数据库表中实际上并没有这个字段
    # backref　表示对应于 Post 表中 post.author 对象
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    """
    'User': 配置关联关系中右边的实体，这里因为是自关联，所以还是‘User’
    secondary: 配置多对多关系中的关联表
    primaryjoin：配置左边实体与关联表的关联条件，左边实体的 id 对应关联表的 follower_id   （关注者）
    secondaryjoin: 配置右边实体与关联表的关联条件，右边实体的 id 对应关联表的 followed_id  （被关注者）
    backref: 定义了如果从右边实体（被关注着）访问关联关系。在左边实体，这里定义为了 followed(被关注者， 意思是这个用户关注了的人)， 所以右边实体定义为followers（关注者， 意思是这个关注了这个用户的人）
    """
    followed = db.relationship('User', secondary=followers,
                               primaryjoin=(followers.c.follower_id == id),
                               secondaryjoin=(followers.c.followed_id == id),
                               backref=db.backref('followers', lazy='dynamic'),
                               lazy='dynamic'
                               )

    def is_following(self, user):
        """
        是否关注了某个用户
        :param user:
        :return:
        """
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def follow(self, user):
        """
        关注某个用户
        :param user:
        :return:
        """
        if not self.is_following(user):
            self.followed.append(user)

    def followed_posts(self):
        """
        获取关注用户和自己的文章
        :return:
        """
        followed_post = Post.query\
            .join(followers, (followers.c.followed_id == Post.user_id))\
            .filter(followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed_post.union(own).order_by(Post.timestamp.desc())

    def unfollow(self, user):
        """
        取消关注
        :param user:
        :return:
        """
        if self.is_following(user):
            self.followed.remove(user)

    def set_password(self, password):
        """
        设置密码
        :param password:
        :return:
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        验证密码
        :param password:
        :return:
        """
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        """
        头像
        :param size:
        :return:
        """
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def get_reset_password_token(self, expires_in=600):
        """
        邮件重置密码获取 token
        :param expires_in:
        :return:
        """
        # exp: 过期时间
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        ).decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms='HS256')['reset_password']
        except :
            # token 无法验证或过期
            return None
        return User.query.get(id)

    # def __repr__(self):
    #     return '<User {}>'.format(self.username)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # def __repr__(self):
    #     return '<Post {}>'.format(self.body)











