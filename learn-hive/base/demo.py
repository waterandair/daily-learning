#!/usr/bin/ python3
# -*- coding: utf-8 -*-
from pyhive import hive  # or import hive
cursor = hive.connect('172.17.0.2').cursor()
cursor.execute('show databases')
print(cursor.fetchone())
print(cursor.fetchall())
