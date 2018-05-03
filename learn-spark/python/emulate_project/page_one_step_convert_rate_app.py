#!/usr/bin/python3
# -*- coding utf-8 -*-
from pyspark import SparkContext
from pyspark.sql import SparkSession
from common.functions import *


if __name__ == '__main__':
    sc = SparkContext("local[1]")
    spark = SparkSession.builder.appName('session_analysis').getOrCreate()
    make_schema(sc, spark)
    # 传入 session 筛选条件,生产中这里应该是从数据库中获取用户在web端提交的task
    # task_params = dict([(line.split(":")[0], line.split(":")[1]) for line in sys.argv[1].split(",")])
    task_params = {
        "start_date": "2018-04-06",
        "end_date": "2018-04-06",
        "start_age": 20,
        "end_age": 50,
        "target_page_flow": "1,2,3,4,5"
        # "professionals": "professional71",
        # "cities": "city20, city2",
        # "gender": "male",
        # "click_category_ids": "54"
    }

    # 按照日期过滤
    action_info_rdd = get_action_rdd_by_date_range(spark, task_params)

    # 按照 session_id 聚合 action 信息
    session_to_actions_rdd = get_session_action_rdd(action_info_rdd).groupByKey()

    # 生成每个 session 单页面跳转切片, (由于是模拟数据,所以很可能出现下游页面访问量大于上游, 转化率可能大于1)
    page_slice_rdd = generate_and_match_page_slice_rdd(session_to_actions_rdd, task_params["target_page_flow"])
    # 计算页面切片的pv量
    page_slice_pv_count = page_slice_rdd.countByKey()
    print(page_slice_pv_count)

    # 计算各个页面切面的转化率
    page_slice_rate = calculate_page_slice_rate(page_slice_pv_count, task_params["target_page_flow"])
    print(page_slice_rate)