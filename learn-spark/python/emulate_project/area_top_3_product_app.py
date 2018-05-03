#!/usr/bin/ python3
# -*- coding: utf-8 -*-
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
        "start_date": "2018-04-17",
        "end_date": "2018-04-17",
        "start_age": 20,
        "end_age": 50,
        "target_page_flow": "1,2,3,4,5"
        # "professionals": "professional71",
        # "cities": "city20, city2",
        # "gender": "male",
        # "click_category_ids": "54"
    }

    # 按照日期过滤
    click_action_rdd = get_click_action_rdd_by_date(spark, task_params)

    # 城市详情rdd, 城市详情一般是存在数据库中的
    caty_id_to_caty_info_rdd = get_caty_id_to_caty_info_rdd(sc)

    # 创建包含 city_id, city_name, area, product_id 的临时表 `tmp_clk_prod_basie`
    schema_temp_click_product = get_temp_click_product_table(spark, click_action_rdd, caty_id_to_caty_info_rdd)

    # 按照 area, product_id 分组, 计算 click_count 创建 `tmp_area_product_click_count`
    schema_temp_area_prdocut_click_count_table(spark)

    # 利用开窗函数从 `tmp_area_product_click_count` 取出每个区域中点击量排名前三的 product_id
    get_area_top3_product_rdd(spark)
