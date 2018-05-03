#!/usr/bin/python3
# -*- coding utf-8 -*-
from pyspark import SparkContext
from pyspark.sql import SparkSession
from common.functions import *
from common.accumulator import SessionAggrAccumulator


if __name__ == '__main__':
    sc = SparkContext("local[1]")
    spark = SparkSession.builder.appName('session_analysis').getOrCreate()
    # 生成 spark sql 表
    make_schema(sc, spark)
    # 传入 session 筛选条件,生产中这里应该是从数据库中获取用户在web端提交的task
    # task_params = dict([(line.split(":")[0], line.split(":")[1]) for line in sys.argv[1].split(",")])
    task_params = {
        "start_date": "2018-04-06",
        "end_date": "2018-04-06",
        "start_age": 20,
        "end_age": 50,
        # "professionals": "professional71",
        # "cities": "city20, city2",
        # "gender": "male",
        # "click_category_ids": "54"
    }

    """
       对于流量较高的应用,用户一天的行为数据可能会有数十亿条,如果不统一筛选粒度,每次都是全表扫描会导致spark性能大降,
       所以这里选择按照 session 粒度对数据进行过滤聚合
       用一些基本的筛选条件,比如时间范围,从 hive 表中提取数据,然后,按照session_id进行聚合,聚合后的一条记录,就是一个用户的某个session
       在指定时间内的访问记录,比如搜索过的所有关键词,点击过的所有品类id, session对应的user_id关联的用户基础信息
    """
    # 按照日期过滤
    action_info_rdd = get_action_rdd_by_date_range(spark, task_params)

    # 按照 session_id 聚合, 先按照 session_id 进行 groupByKey 分组, 再与用户信息进行join
    session_id_aggr_info_rdd = aggregate_by_session(spark, action_info_rdd)
    # session_id_aggr_info_rdd.foreach(lambda row: print(row))
    # ('459737a2f23a4d4ebec1a550a4344a85', 'session_id=459737a2f23a4d4ebec1a550a4344a85|search_keys=,呷哺呷哺,重庆小面,国贸大厦,蛋糕,重庆辣子鸡,温泉,日本料理,新辣道鱼火锅,太古商场|click_category_ids=,49,59,87,75|age=39|professional=professional76|city=city57|gender=female')

    # 创建计算 访问时长 和 访问步长 的累加器

    accum = sc.accumulator("", accum_param=SessionAggrAccumulator())

    # 按照条件过滤 session 粒度的数据
    filter_session_id_aggr_info_rdd = filter_session(session_id_aggr_info_rdd, task_params, accum)
    # filter_session_id_aggr_info_rdd.foreach(lambda row: print(row))
    # print(filter_session_id_aggr_info_rdd.count())  # 累加操作前必须先执行 action 算子
    # print("访问时长和访问步长:", accum.value)

    # 按照时间比例随机抽取 sessionid
    extract_sessionids_rdd = random_extract_session(filter_session_id_aggr_info_rdd)
    #extract_sessionids_rdd.foreach(lambda row: print(row))
    # print(extract_sessionids_rdd.count())

    # 获取 session 对应 action 的 rdd
    session_action_rdd = get_session_action_rdd(action_info_rdd)

    # 通过筛选条件的session 的 访问明细数据
    filter_session_action_detail_rdd = filter_session_action_detail_rdd(filter_session_id_aggr_info_rdd,
                                                                        session_action_rdd)

    # 获取 top10 品类, 根据点击量, 下单量, 支付量排序
    sorted_category_rdd = get_sorted_category_rdd(filter_session_id_aggr_info_rdd, session_action_rdd)
    top_10_category_list = sorted_category_rdd.take(10)
    # print(top_10_category_list)

    # 获取top10品类的 top10 session, 根据点击量
    top_10_category_session_click_count = get_sorted_category_click_session_rdd(sc,
                                                                                top_10_category_list,
                                                                                filter_session_action_detail_rdd,
                                                                                10)
    top_10_category_session_click_count.foreach(print)








