#!/usr/bin/ python3
# -*- coding: utf-8 -*-
from flask import Blueprint

bp = Blueprint('errors', __name__)

# 在底部导入，避免循环依赖
from app.errors import handlers
