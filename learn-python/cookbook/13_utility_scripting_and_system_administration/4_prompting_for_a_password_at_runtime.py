#!/usr/bin/python3
# coding utf-8
import getpass
user = getpass.getuser()
password = getpass.getpass()


def svc_login(user, password):
    return True


if svc_login(user, password):
    print('ok')
else:
    print('no')
