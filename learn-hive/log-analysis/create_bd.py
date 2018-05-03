#!/usr/bin/ python3
# -*- coding: utf-8 -*-
import ibis
hive_client = ibis.impala.connect('172.17.0.2', 10000, user='root', auth_mechanism='PLAIN', database='default')

# 创建日志表
sql = "CREATE TABLE IF NOT EXISTS default.logs_src (" \
      "remote_addr STRING," \
      "remote_user STRING," \
      "time_local STRING," \
      "request STRING," \
      "status STRING," \
      "body_bytes_sent STRING," \
      "http_user_agent STRING)" \
      "ROW FORMAT DELIMITED FIELDS TERMINATED BY ' '" \
      "STORED AS textfile"
hive_client.raw_sql(sql)

