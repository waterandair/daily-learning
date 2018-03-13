#!/usr/bin/python3
# -*- coding utf-8 -*-
from urllib.request import urlopen
"""
In many cases, single-method classes can be turned into functions using closures.Consider, as an example, the following
class, witch allows a user to fetch URLs using a kind of  templating scheme.
"""
class UrlTemplate:
    def __init__(self, template):
        self.template = template

    def open(self, **kwargs):
        return urlopen(self.template.format_map(kwargs))


def urltemplate(template):
    def opener(**kwargs):
        return urlopen(template.format_map(kwargs))
    return opener