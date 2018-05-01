#!/usr/bin/python3
from flask import render_template, flash, redirect, url_for, request, session
from app import db
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app.auth.forms import LoginForm, RegistrationFrom, ResetPasswordRequestForm, ResetPasswordForm
from app.models import User
from app.auth.email import send_password_reset_email
from app.auth import bp


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("无效的用户名或密码")
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)

        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        flash(current_user.username)
        flash(current_user.is_authenticated)
        flash(session.get('user_id'))
        return redirect(next_page)
    return render_template('auth/login.html', form=form, title='登录')


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationFrom()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("注册成功")
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', title='注册', form=form)


@bp.route('/reset_password_request', methods=['GET','POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('重置链接已经发到邮箱，点击链接重置密码')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_request.html', title='重置密码', form=form)


@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    user = User.verify_reset_password_token(token)
    if not user:
        flash("无效的请求或过期的请求")
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('密码重置成功')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)














