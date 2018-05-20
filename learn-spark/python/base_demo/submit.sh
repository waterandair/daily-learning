#!/usr/bin/env bash
spark-submit \
  --master local[2] \
  /home/zj/project/daily-learning/learn-spark/python/base_demo/streaming/updateStateByKeyWorldCount.py