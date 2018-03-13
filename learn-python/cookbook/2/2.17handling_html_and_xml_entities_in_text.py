#!/usr/bin/python3
# -*- coding utf-8 -*-
import html
from xml.sax.saxutils import unescape

# If you are producing text, replacing special characters such as < or > is relatively easy if you use the html.escape()
# function

s = 'Elements are written as "<tag>text</tag>".'
print(html.escape(s))  # Elements are written as &quot;&lt;tag&gt;text&lt;/tag&gt;&quot;.
# Disable escaping of quotes
print(html.escape(s, quote=False))  # Elements are written as "&lt;tag&gt;text&lt;/tag&gt;".


s = 'Spicy Jalapeño'
res = s.encode('ascii', errors='xmlcharrefreplace')
print(res)  # b'Spicy Jalape&#241;o'


s = 'Spicy &quot;Jalape&#241;o&quot.'
print(html.unescape(s))  # 'Spicy "Jalapeño".'


t = 'The prompt is &gt;&gt;&gt;'
print(unescape(t))  # The prompt is >>>
