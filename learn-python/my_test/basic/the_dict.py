#!/usr/bin/python
# -*- coding utf-8 -*-

d = {
    'kobe': 37,
    'wade': 34,
    't-mac': 38,
    #'ai': -1
}
# d.get('ai', -1) 取倒数第一个键值，如果没有返回第二个参数指定的值，如果没有第二个参数，返回 None
print('''
d[\'kobe\'] = %s
d[\'wade\'] = %s
d[\'t-mac\'] = %s
d.get(\'ai\', -1) = %d
''' % (d['kobe'], d['wade'], d['t-mac'], d.get('ai')))
