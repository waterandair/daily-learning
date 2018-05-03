#!/usr/bin/ python3
# -*- coding: utf-8 -*-
import ibis

#hdfs_client = ibis.hdfs_connect('172.17.0.2', 9870)
# print(hdfs_client.ls('/'))

hive_client = ibis.impala.connect('172.17.0.2', 10000, auth_mechanism='PLAIN', user='root', database='default')
hive_client.create_database('test')