#!/usr/bin/python3
# -*- coding utf-8 -*-
import os
from datetime import datetime
from functools import reduce
import random
from pyspark.sql.types import StructField, StructType, StringType,Row
import numpy as np
from common.constant import *


def multiple_in(full_str, sub_str):
    """
    判断一个逗号分割的字符串中的子项是否都在另一个逗号分割的字符串中能找到
    :param full_str: 被寻找的字符串
    :param sub_str: 要寻找的字符串
    :return:
    """
    full_list = full_str.split(",")
    sub_list = sub_str.split(",")
    if len(full_list) == 0 or len(sub_list) == 0:
        return False
    res = True
    for sub in sub_list:
        if full_list.count(sub) == 0:
            res = False
            break
    return res


def make_schema(sc, spark):
    """
    创建模拟数据
    :param sc:
    :param spark:
    :return:
    """
    make_user_visit_action_schema(sc, spark)
    make_user_info_schema(sc, spark)


def make_user_visit_action_schema(sc, spark):
    """
    创建模拟 user_visit_action 表
    :param sc:
    :param spark:
    :return:
    """
    path = os.path.dirname(os.path.realpath(__file__))

    user_visit_action_rdd = sc.textFile("file://" + path + "/session_analysis_data.txt")
    user_visit_action_data = user_visit_action_rdd.map(lambda line: tuple(line.split(",")))
    # 定义字段
    schema_user_visit_action_string = "date userid sessionid page_id action_time search_key_word click_category_id " + \
        "click_product_id order_category_ids order_product_ids pay_category_ids pay_product_ids city_id"
    fields = [StructField(field_name, StringType(), True) for field_name in schema_user_visit_action_string.split()]
    schema = StructType(fields)

    schema_user_visit_action = spark.createDataFrame(user_visit_action_data, schema)
    schema_user_visit_action.createOrReplaceTempView("user_visit_action")
    # results = spark.sql("select * from user_visit_action")
    # results.show()


def make_user_info_schema(sc, spark):
    """
    创建模拟 user_info 表
    :param sc:
    :param spark:
    :return:
    """
    path = os.path.dirname(os.path.realpath(__file__))

    user_info_rdd = sc.textFile("file://" + path + "/user_info.txt")
    user_info_data = user_info_rdd.map(lambda line: tuple(line.split(",")))
    # 定义字段
    schema_user_info_string = "userid username name age professional city gender"
    fields = [StructField(field_name, StringType(), True) for field_name in schema_user_info_string.split()]
    schema = StructType(fields)

    schema_user_info = spark.createDataFrame(user_info_data, schema)
    schema_user_info.createOrReplaceTempView("user_info")
    # results = spark.sql("select * from user_info")
    # results.show()


def get_action_rdd_by_date_range(spark, task_params):
    """
    按照日期过滤 action 数据
    :param spark:
    :param task_params:
    :return:
    """
    start_date = task_params[PARAM_START_DATE]
    end_date = task_params[PARAM_END_DATE]
    sql_str = "SELECT * FROM user_visit_action WHERE date >='" + start_date + "' AND date<='" + end_date + "'"
    action_df = spark.sql(sql_str)
    return action_df.rdd


def get_session_action_rdd(action_rdd):
    """
    获取 <session_id, aggr_info<>> 的rdd
    :param action_rdd:
    :return:
    """
    session_action_rdd = action_rdd.map(lambda row: (row[2], row))
    return session_action_rdd


def aggregate_by_session(spark, action_info_rdd):
    """
    按照 session 聚合 action 数据和用信息
    :param spark:
    :param action_info_rdd:
    :return:
    """
    # 按照 session_id 进行分组
    session_id_aggr_info_rdd = action_info_rdd\
        .map(lambda row: (row[2], row))\
        .groupByKey()
    # 对每一个session分组进行聚合,将所有的搜索词和点击品类都聚合起来
    def aggregate_session_action_info(row):
        session_id = row[0]
        actions = row[1]

        user_id = ''
        search_keys = []
        click_categories = []

        # session 的起始时间和结束时间
        start_time = None
        end_time = None
        # session 的访问步长(一个session中的action个数)
        step_length = 0

        for action in actions:
            if user_id == '':
                user_id = action[1]
            search_key = action[5]
            click_category = action[6]
            if search_key != "" and search_keys.count(search_key) == 0:
                search_keys.append(search_key)
            if click_category != '' and click_categories.count(click_category) == 0:
                click_categories.append(click_category)

            # 计算 session 开始和结束的时间 时间格式:2018-04-06 04:03:43
            action_time = datetime.strptime(action[4], '%Y-%m-%d %H:%M:%S')
            if start_time is None and end_time is None:
                start_time, end_time = action_time, action_time
            if action_time < start_time:
                start_time = action_time
            if action_time > end_time:
                end_time = action_time

            # 计算步长
            step_length += 1

        search_keys_str = ",".join(search_keys)
        click_categories_str = ",".join(click_categories)

        # 访问时长(秒)
        visit_length = (end_time - start_time).seconds

        # aggr_info_str = "session_id=" + session_id + \
        #                 "|search_keys=" + search_keys_str + \
        #                 "|click_category_ids=" + click_categories_str
        aggr_info_dict = {
            FIELD_SESSION_ID: session_id,
            FIELD_SEARCH_KEYWORDS: search_keys_str,
            FIELD_CLICK_CATEGORY_IDS: click_categories_str,
            FIELD_VISIT_LENGTH: visit_length,
            FIELD_STEP_LENGTH: step_length,
            FIELD_START_TIME: str(start_time)
        }
        return user_id, aggr_info_dict

    # 为了和用户信息聚合,这里组织一个 (user_id, aggr_info) 的数据对
    user_id_aggr_info_rdd = session_id_aggr_info_rdd.map(lambda row: aggregate_session_action_info(row))

    user_sql = "SELECT * FROM user_info"
    user_info_rdd = spark.sql(user_sql).rdd
    # 组织成一个 (user_id, row) 的数据对
    user_info_rdd = user_info_rdd.map(lambda row: (row[0], row))

    # 将 session 粒度聚合的数据与 user 信息进行 join
    user_full_info_rdd = user_id_aggr_info_rdd.join(user_info_rdd)
    # 整理聚合的信息

    def get_full_aggreate_info(row):
        # session粒度聚合的数据
        part_aggr_info = row[1][0]
        # user 信息
        user_info = row[1][1]
        user_id = row[0]

        session_id = part_aggr_info[FIELD_SESSION_ID]
        age = user_info[3]
        professional = user_info[4]
        city = user_info[5]
        gender = user_info[6]
        user_info_dict = {
            FIELD_AGE: age,
            FIELD_PROFESSIONAL: professional,
            FIELD_CITY: city,
            FIELD_GENDER: gender,
            FIELD_USER_ID: user_id
        }
        part_aggr_info.update(user_info_dict)
        return session_id, part_aggr_info

    return user_full_info_rdd.map(lambda row: get_full_aggreate_info(row))


def filter_session(session_id_aggr_info_rdd, task_params, accmu):
    """
    按照条件过滤 session 粒度的数据
    :param session_id_aggr_info_rdd:
    :param task_params:
    :return:
    """
    def filter_rdd(row):
        """
        过滤并统计访问时长和步长
        :param row:
        :return:
        """
        aggr_info_dict = row[1]
        res = True
        # 按照年龄范围进行过滤
        if task_params.get(PARAM_START_AGE) is not None and task_params.get(PARAM_END_AGE) is not None:
            if int(task_params[PARAM_START_AGE]) < int(aggr_info_dict[FIELD_AGE]) < int(task_params[PARAM_END_AGE]):
                res = False
        # 按照职业范围进行过滤
        if task_params.get(PARAM_PROFESSIONALS) and \
                task_params[PARAM_PROFESSIONALS].split(",").count(aggr_info_dict[FIELD_PROFESSIONAL]) < 1:
            res = False
        # 按照城市范围过滤
        if task_params.get(PARAM_CITIES) and \
                task_params[PARAM_CITIES].split(",").count(aggr_info_dict[FIELD_CITY]) < 1:
            res = False
        # 按照性别范围过滤
        if task_params.get(PARAM_GENDER) and \
                task_params[PARAM_GENDER] != aggr_info_dict[FIELD_GENDER]:
            res = False
        # 按照搜索词进行过滤
        if task_params.get(PARAM_KEYWORDS) and \
                not multiple_in(aggr_info_dict[FIELD_SEARCH_KEYWORDS], task_params[PARAM_KEYWORDS]):
            res = False
        # 按照点击品类 id 进行过滤
        if task_params.get(FIELD_CLICK_CATEGORY_IDS) and \
                not multiple_in(aggr_info_dict[FIELD_CLICK_CATEGORY_IDS], task_params[FIELD_CLICK_CATEGORY_IDS]):
            res = False

        # 统计访问时长和访问步长
        accmu.add(SESSION_COUNT)
        visit_length = aggr_info_dict.get(FIELD_VISIT_LENGTH)
        step_length = aggr_info_dict.get(FIELD_STEP_LENGTH)
        if 1 <= visit_length <= 3:
            accmu.add(TIME_PERIOD_1s_3s)
        elif 4 <= visit_length <= 6:
            accmu.add(TIME_PERIOD_4s_6s)
        elif 7 <= visit_length <= 9:
            accmu.add(TIME_PERIOD_7s_9s)
        elif 10 <= visit_length <= 30:
            accmu.add(TIME_PERIOD_10s_30s)
        elif 30 < visit_length <= 60:
            accmu.add(TIME_PERIOD_30s_60s)
        elif 60 < visit_length <= 180:
            accmu.add(TIME_PERIOD_1m_3m)
        elif 180 < visit_length <= 600:
            accmu.add(TIME_PERIOD_3m_10m)
        elif 600 < visit_length <= 1800:
            accmu.add(TIME_PERIOD_10m_30m)
        elif 1800 < visit_length:
            accmu.add(TIME_PERIOD_30m)

        if 1 <= step_length <= 3:
            accmu.add(STEP_PERIOD_1_3)
        elif 4 <= step_length <= 6:
            accmu.add(STEP_PERIOD_4_6)
        elif 7 <= step_length <= 9:
            accmu.add(STEP_PERIOD_7_9)
        elif 10 <= step_length <= 30:
            accmu.add(STEP_PERIOD_10_30)
        elif 30 < step_length <= 60:
            accmu.add(STEP_PERIOD_30_60)
        elif step_length > 60:
            accmu.add(STEP_PERIOD_60)

        return res

    filter_session_id_aggr_info_rdd = session_id_aggr_info_rdd.filter(lambda row: filter_rdd(row))
    return filter_session_id_aggr_info_rdd


def random_extract_session(session_id_aggr_info_rdd):
    def get_time_session_id_rdd(row):
        aggr_info = row[1]
        start_time = datetime.strptime(aggr_info[FIELD_START_TIME], '%Y-%m-%d %H:%M:%S')
        start_time = start_time.strftime('%Y-%m-%d_%H')
        # 格式 <yyyy-MM-dd_HH,count>
        return start_time, aggr_info
    # 获取格式为 <yyyy-MM-dd_HH,count> 的rdd
    time_session_id_rdd = session_id_aggr_info_rdd.map(lambda row: get_time_session_id_rdd(row))
    count_session_by_hour = time_session_id_rdd.countByKey()

    # 格式转换为 <yyyy-MM-dd,{HH:count,HH:count, ...}>
    date_hour_counts = {}
    for date_hour, count in count_session_by_hour.items():
        date = date_hour.split("_")[0]
        hour = date_hour.split("_")[1]

        hour_counts = date_hour_counts.get(date)
        if hour_counts is None:
            date_hour_counts[date] = {}
        date_hour_counts[date].update({hour: count})
    # print(date_hour_counts)

    # 计算每天要抽取的数量
    extract_pre_day_nums = PARAM_EXTRACT_NUMS // len(date_hour_counts)

    # 格式: {date:{hour:[1, 2, 3, ...], hour:[1, 2, 3, ...]}, ...}
    date_hour_extract = {}

    for date, hour_counts in date_hour_counts.items():
        # 这一天的session总数
        total_counts = reduce(lambda v1, v2: v1 + v2, hour_counts.values())

        # 格式: {hour:[1, 2, 3, ...], hour:[1, 2, 3, ...]}  # 每个小时对应要抽取session的索引
        hour_extract = date_hour_extract.get(date)
        if hour_extract is None:
            date_hour_extract[date] = {}

        # 遍历每个小时
        for hour, count in hour_counts.items():
            # 计算每个小时的 session 数量占据当天总session数量的比例,直接乘以每天要抽取的数量,就可以计算出,当前小时需要抽取的session数量
            hour_extract_num = int((count / total_counts) * extract_pre_day_nums)

            if hour_extract_num > count:
                hour_extract_num = count
            # print("hour_extract_num", hour_extract_num)
            hour_extract_list = date_hour_extract[date].get(hour)
            if hour_extract_list is None:
                date_hour_extract[date][hour] = []

            # 生成随机索引
            for i in range(hour_extract_num):
                extract_index = random.randint(0, count-1)
                while date_hour_extract[date][hour].count(extract_index) >= 1:
                    extract_index = random.randint(0, count - 1)

                date_hour_extract[date][hour].append(extract_index)

    # 遍历每天每小时的session, 根据随机索引进行抽取
    times_sessionids_rdd = time_session_id_rdd.groupByKey()

    # 获取抽取出的 session_id
    def get_extract_sessionids_rdd(row):
        # 所有抽取出的session_id
        extract_sessionids = []
        date = row[0].split("_")[0]
        hour = row[0].split("_")[1]
        aggrs = (x for x in row[1])

        index = 0
        extract_index_list = date_hour_extract.get(date).get(hour)
        for aggr in aggrs:
            if extract_index_list.count(index) >= 1:
                # 在这里抽取出session_id, 同时可以进行持久化操作,比如插入数据库
                session_id = aggr[FIELD_SESSION_ID]
                extract_sessionids.append(session_id)
            index += 1
        return extract_sessionids

    extract_sessionids_rdd = times_sessionids_rdd.flatMap(lambda row: get_extract_sessionids_rdd(row))
    return extract_sessionids_rdd


def get_sorted_category_rdd(filter_session_rdd, session_action_rdd):

    # 1. 获取符合条件的session 的访问明细 格式 <session_id, <action_infos>>
    session_detail_rdd = filter_session_rdd\
        .join(session_action_rdd).\
        map(lambda row: (row[0], row[1][1]))

    def get_all_category_id(row):
        action = row[1]
        category_id_list = []

        # 点击过的 品类id
        click_category_id = action[6]
        if click_category_id != '':
            category_id_list.append((click_category_id, click_category_id))

        # 下单过的 品类id
        order_category_ids = action[8]
        if order_category_ids != '':
            order_category_ids_list = order_category_ids.split(",")
            map(lambda item: category_id_list.append(item), order_category_ids_list)

        pay_category_ids = action[10]
        if pay_category_ids != '':
            pay_category_ids_list = pay_category_ids.split(",")
            map(lambda item: category_id_list.append(item), pay_category_ids_list)

        return category_id_list

    # 2. 获取访问过的所有 category_id, (点击过,下单过,支付过的品类)
    category_ids_rdd = session_detail_rdd\
        .flatMap(lambda row: get_all_category_id(row))\
        .distinct()

    # 3. 分别计算点击品类的次数, 下单品类的次数, 支付品类的次数, 并合并在一个rdd中
    click_category_id_count_rdd = get_click_category_id_count_rdd(session_detail_rdd)
    order_category_id_count_rdd = get_order_category_id_count_rdd(session_detail_rdd)
    pay_category_id_count_rdd = get_pay_category_id_count_rdd(session_detail_rdd)
    category_id_count_rdd = get_join_category_count_rdd(category_ids_rdd,
                                                click_category_id_count_rdd,
                                                order_category_id_count_rdd,
                                                pay_category_id_count_rdd)

    # 4. 按照 点击,下单,支付, 的顺序排序
    sorted_category_count_rdd = get_sorted_category_count_rdd(category_id_count_rdd)
    return sorted_category_count_rdd
    

# 计算各品类的点击次数
def get_click_category_id_count_rdd(session_detail_rdd):
    click_category_id_count_rdd = session_detail_rdd\
        .filter(lambda row: row[1][6] != '')\
        .map(lambda row: (row[1][6], 1))\
        .reduceByKey(lambda a, b: a + b)
    return click_category_id_count_rdd


# 计算各品类下单的次数
def get_order_category_id_count_rdd(session_detail_rdd):
    order_category_id_count_rdd = session_detail_rdd\
        .filter(lambda row: row[1][8] != '')\
        .flatMap(lambda row: list(map(lambda item: (item, 1), row[1][8].split(","))))\
        .reduceByKey(lambda a, b: a + b)
    return order_category_id_count_rdd


# 计算各品类支付的次数
def get_pay_category_id_count_rdd(session_detail_rdd):
    pay_category_id_count_rdd = session_detail_rdd \
        .filter(lambda row: row[1][10] != '') \
        .flatMap(lambda row: list(map(lambda item: (item, 1), row[1][10].split(",")))) \
        .reduceByKey(lambda a, b: a + b)
    return pay_category_id_count_rdd


# 合并品类id 和 点击,下单,支付数
def get_join_category_count_rdd(category_ids_rdd, click_category_count_rdd, order_category_count_rdd, pay_category_count_rdd):
    category_id_count_rdd = category_ids_rdd\
        .leftOuterJoin(click_category_count_rdd)\
        .map(lambda row: (row[0], {FIELD_CATEGORY_ID: row[0], FIELD_CLICK_COUNT: row[1][1]}))\
        .leftOuterJoin(order_category_count_rdd)\
        .map(lambda row: (row[0], row[1][0] if row[1][0].update({FIELD_ORDER_COUNT: row[1][1]}) is None else {}))\
        .leftOuterJoin(pay_category_count_rdd)\
        .map(lambda row: (row[0], row[1][0] if row[1][0].update({FIELD_PAY_COUNT: row[1][1]}) is None else {}))
    return category_id_count_rdd


# 按照 点击,下单,支付 中品类计数进行倒序排序
def get_sorted_category_count_rdd(category_count_rdd):
    sort_key_to_category_count_rdd = category_count_rdd.map(lambda row:
                                                            (
                                                                (
                                                                    row[1][FIELD_CLICK_COUNT],
                                                                    row[1][FIELD_ORDER_COUNT],
                                                                    row[1][FIELD_PAY_COUNT]
                                                                ),
                                                                row[1]
                                                            ))
    sorted_category_count_rdd = sort_key_to_category_count_rdd.sortByKey(ascending=False)
    return sorted_category_count_rdd


# 获取session对应的action明细
def filter_session_action_detail_rdd(filter_session_id_aggr_info_rdd,  session_action_rdd):
    session_detail_rdd = filter_session_id_aggr_info_rdd\
        .join(session_action_rdd)\
        .map(lambda row: (row[0], row[1][1]))
    return session_detail_rdd


# 获取指定品类中按照 点击量 排序的session
def get_sorted_category_click_session_rdd(sc, top_category_list, session_detail_rdd, top_n):

    # 获取 category_id, 并组成 rdd
    category_id_list = []
    for item in top_category_list:
        category_id_list.append((item[1][FIELD_CATEGORY_ID], item[1][FIELD_CATEGORY_ID]))

    category_id_rdd = sc.parallelize(category_id_list)

    # 获取 session 对每个品类的点击次数的rdd : <category_id, <session_id, click_count>>
    def get_session_category_click_count(row):
        res = []
        for action in row[1]:
            if action[6] != '':
                res.append(action[6])
        # 获取到 [(category_id, click_count),]
        res = list(zip(*np.unique(res, return_counts=True)))
        # 转换为  <category_id, <session_id, click_count>>
        category_session_click_count = [(items[0], (row[0], items[1])) for items in res]
        return category_session_click_count

    category_click_session_rdd = session_detail_rdd\
        .groupByKey()\
        .flatMap(lambda row: get_session_category_click_count(row))

    # 获取每个品类, 被各个 session 点击的次数
    category_session_click_count_rdd = category_id_rdd\
        .join(category_click_session_rdd)\
        .map(lambda row: (row[0], row[1][1]))\
        .groupByKey()

    # 分组取 topN
    def get_top_n_category_session(row):
        sorted_session_click_count = sorted(row[1], key=lambda x: x[1], reverse=True)
        top_n_session_click_count = sorted_session_click_count[:top_n]
        return row[0], top_n_session_click_count

    top_n_category_session_rdd = category_session_click_count_rdd.map(lambda row: get_top_n_category_session(row))
    return top_n_category_session_rdd


"""
页面单跳转化率
"""


def generate_and_match_page_slice_rdd(session_to_actions_rdd, target_page_flow):

    # 生成页面切片的rdd
    def get_rows(row):
        # 页面切片计数. 例如[("1_2", 1), ("2_3", 1), ("1_2", 1)], 这里规定其实页面的切片为 0_[start_page_id]
        page_slice_list = []
        actions = row[1]
        # 获取指定的页面流 例如:1,2,3,4,5
        target_pages = target_page_flow.split(",")
        # 获取起始页面id
        start_page_id = target_pages[0]
        # 获取页面流切片, 例如 [1_2, 2_3, 3_4, 4_5]
        target_pages = [target_pages[i-1] + "_" + target_pages[i] for i in range(1, len(target_pages))]
        # 按照时间对 actions 排序
        actions_sort_by_action_time = sorted(actions, key=lambda action: action[4])

        # 获取 action 中匹配目标页面切片的项
        last_page_id = None
        for action in actions_sort_by_action_time:

            page_id = action[3]
            # 计算起始页面的访问量
            if page_id == start_page_id:
                page_slice_list.append(("0_" + start_page_id, 1))

            if last_page_id is None:
                last_page_id = page_id
                continue

            # 相邻两个 action 组成的 页面切片, 计算页面切片的访问量
            page_slice = last_page_id + "_" + page_id
            if target_pages.count(page_slice) >= 1:
                page_slice_list.append((page_slice, 1))
            last_page_id = page_id

        return page_slice_list

    res_rdd = session_to_actions_rdd.flatMap(lambda row: get_rows(row))
    return res_rdd


# 计算页面流的转化率
def calculate_page_slice_rate(page_slice_pv_count, target_page_flow):
    target_pages = target_page_flow.split(",")
    # 获取起始页面id
    start_page_id = target_pages[0]
    # 获取页面流切片, 例如 [1_2, 2_3, 3_4, 4_5]
    target_pages = [target_pages[i - 1] + "_" + target_pages[i] for i in range(1, len(target_pages))]
    # 起始页 pv
    start_page_pv_count = page_slice_pv_count["0_" + start_page_id]

    # 记录各个页面切片的转化率
    convert_rate_list = []
    last_page_slice_count = 0
    for page_slice in target_pages:

        if target_pages.index(page_slice) == 0:
            convert_rate = format(page_slice_pv_count[page_slice] / start_page_pv_count, '0.2f')
        else:
            convert_rate = format(page_slice_pv_count[page_slice] / last_page_slice_count, '0.2f')

        convert_rate_list.append((page_slice, convert_rate))
        last_page_slice_count = page_slice_pv_count[page_slice]

    return convert_rate_list


"""
各区域热门商品统计
"""


def get_click_action_rdd_by_date(spark, task_params):
    """
    按照日期和是否点击商品过滤 action 数据
    :param spark:
    :param task_params:
    :return:
    """
    start_date = task_params[PARAM_START_DATE]
    end_date = task_params[PARAM_END_DATE]
    sql_str = "SELECT city_id, click_product_id as product_id  FROM user_visit_action WHERE click_product_id != '' AND  date >='" + start_date + "' AND date<='" + end_date + "'"
    action_df = spark.sql(sql_str)
    return action_df.rdd.map(lambda row: (int(row[0]), row))


def get_caty_id_to_caty_info_rdd(sc):
    """
    获取城市详细信息
    :param sc:
    :return:
    """
    # 城市详细信息(id,(id,name,area))
    caty_info = [
        (0, (0, '北京', '华北')),
        (1, (1, '上海', '华东')),
        (2, (2, '南京', '华东')),
        (3, (3, '广州', '华南')),
        (4, (4, '三亚', '华南')),
        (5, (5, '武汉', '华中')),
        (6, (6, '长沙', '华中')),
        (7, (7, '西安', '西北')),
        (8, (8, '成都', '西南')),
        (9, (9, '哈尔滨', '东北'))

    ]
    return sc.parallelize(caty_info)


def get_temp_click_product_table(spark, click_action_rdd, city_id_to_city_info_rdd):
    """
    把 rdd 合并得到每次action的city_id和product_id, 并转化为临时表
    :param spark:
    :param click_action_rdd:
    :param city_id_to_city_info_rdd:
    :return:
    """
    print(click_action_rdd.take(3))
    print(city_id_to_city_info_rdd.take(3))
    temp_click_product_rdd = click_action_rdd\
        .join(city_id_to_city_info_rdd)\
        .map(lambda row: Row(city_id=row[0], city_name=row[1][1][1], area=row[1][1][2], product_id=row[1][0][1]))

    schema_click_product = spark.createDataFrame(temp_click_product_rdd)
    schema_click_product.createOrReplaceTempView("tmp_clk_prod_basic")
    # schema_click_product.show()


def schema_temp_area_prdocut_click_count_table(spark):
    """
    生成各区域各商品点击次数临时表
    :param spark:
    :return:
    """
    sql = "SELECT " \
          "area, " \
          "product_id, " \
          "count(*) as click_count, " \
          "collect_set(concat(city_id, ':', city_name)) as city_info " \
          "FROM tmp_clk_prod_basic " \
          "GROUP BY area, product_id"
    df = spark.sql(sql)
    df.createOrReplaceTempView("tmp_area_product_click_count")
    # spark.sql("SELECT * from tmp_area_product_click_count").show()
    # +----+----------+-----------+--------------------------+
    # | area | product_id | click_count | city_infos |
    # +----+----------+-----------+--------------------------+
    # | 华东  | 14         | 21          | [2: 南京, 1: 上海] |
    # | 华中  | 11         | 22          | [6: 长沙, 5: 武汉] |
    # | 华北  | 13         | 15          | [0: 北京]         |


def get_area_top3_product_rdd(spark):
    """
    获取各区域 top3 商品
    先使用开窗函数进行一个子查询, 查询出一个 每个区域内 商品的 click_count 按照倒序排序的结果集
    然后在得到的结果集中,取每个区域中 行号 1-3 的行
    :param spark:
    :return:
    """
    sql = "SELECT " \
            "area, " \
            "CASE " \
                "WHEN area='华北' OR area='华东' THEN 'A级' " \
                "WHEN area='华中' OR area='华南'  THEN 'B级' " \
                "WHEN area='西北' OR area='西南'  THEN 'C级' " \
                "ELSE 'D级'" \
            "END area_level, " \
          "product_id, " \
          "click_count, " \
          "city_info " \
          "FROM " \
            "(" \
                "SELECT " \
                    "area, " \
                    "product_id, " \
                    "click_count, " \
                    "city_info, " \
                    "row_number() OVER(PARTITION BY area ORDER BY click_count DESC ) as rank " \
                    "FROM tmp_area_product_click_count) AS t " \
          "WHERE rank <=3"

    df = spark.sql(sql)
    df.show()
    # |area|area_level|product_id|click_count|   city_info|
    # +----+----------+----------+-----------+------------+
    # |  华东|        A级|        24|         34|[2:南京, 1:上海]|
    # |  华东|        A级|        44|         33|[2:南京, 1:上海]|
    # |  华东|        A级|        65|         31|[2:南京, 1:上海]|
    # |  西北|        C级|        32|         21|      [7:西安]|
    # |  西北|        C级|        92|         20|      [7:西安]|
    # |  西北|        C级|         4|         18|      [7:西安]|
    # |  华南|        B级|        19|         34|[4:三亚, 3:广州]|
    # |  华南|        B级|        76|         31|[4:三亚, 3:广州]|
    # |  华南|        B级|        49|         31|[4:三亚, 3:广州]|
    # |  华北|        A级|        87|         29|      [0:北京]|
    # |  华北|        A级|        57|         25|      [0:北京]|
    # |  华北|        A级|        44|         24|      [0:北京]|
    # |  东北|        D级|        84|         19|     [9:哈尔滨]|
    # |  东北|        D级|        15|         18|     [9:哈尔滨]|
    # |  东北|        D级|        33|         18|     [9:哈尔滨]|
    # |  华中|        B级|        32|         40|[6:长沙, 5:武汉]|
    # |  华中|        B级|        43|         37|[6:长沙, 5:武汉]|
    # |  华中|        B级|        25|         37|[6:长沙, 5:武汉]|
    # |  西南|        C级|        99|         29|      [8:成都]|
    # |  西南|        C级|        71|         27|      [8:成都]|
    # +----+----------+----------+-----------+------------+






















