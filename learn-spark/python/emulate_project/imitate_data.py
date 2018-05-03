#!/usr/bin/python3
# -*- coding utf-8 -*-
import datetime
import random
import uuid
import os
path = os.path.dirname(os.path.realpath(__file__))
# 生成的模拟用户行为数据的文件位置
user_visit_actions_filename = path + '/user_visit_actions.txt'
# 生成的模拟用户信息数据的文件位置
user_info_filename = path + '/user_info.txt'


def imitate_data():
    """
    生成用户行为模拟数据
    :return:
    """
    rows = []
    # 用户搜索行为中搜索的关键字
    search_key_words = ["火锅", "蛋糕", "重庆辣子鸡", "重庆小面", "呷哺呷哺", "新辣道鱼火锅", "国贸大厦", "太古商场", "日本料理", "温泉"]
    date = datetime.date.today().strftime("%Y-%m-%d")
    # 用户行为类别
    actions = ["search", "click", "order", "pay"]

    for i in range(100):
        # 用户id
        userid = str(random.randint(1, 100))
        city_id = str(random.randint(0, 9))

        for j in range(10):
            # 使用随机 uuid 模拟 session_id, 代表某次访问事件
            sessionid = str(uuid.uuid4()).replace("-", "")
            base_action_time = date + " " + str(random.randint(0, 23)).zfill(2)

            for k in range(random.randint(1, 100)):
                # 分页id
                page_id = str(random.randint(1, 10))
                # 点击行为发生的具体时间
                action_time = base_action_time + ":" + \
                    str(random.randint(0, 59)).zfill(2) + ":" + \
                    str(random.randint(0, 59)).zfill(2)
                # 如果是搜索行为,这里是搜索关键字
                search_key_word = ''
                # 在网站首页点击了某个品类
                click_category_id = ''
                # 可能是在网站首页或商品列表点击了某个商品
                click_product_id = ''
                # 订单中的商品的品类
                order_category_ids = ''
                # 订单中的商品
                order_product_ids = ''
                # 某次支付行为下所有商品的品类
                pay_category_ids = ''
                # 某次支付行为中的所有商品
                pay_product_ids = ''
                action = actions[random.randint(0, 3)]

                if action == 'search':
                    search_key_word = search_key_words[random.randint(0, 9)]
                elif action == 'click':
                    click_category_id = str(random.randint(1, 100))
                    click_product_id = str(random.randint(1, 100))
                elif action == 'order':
                    order_category_ids = str(random.randint(1, 100))
                    order_product_ids = str(random.randint(1, 100))
                elif action == 'pay':
                    pay_category_ids = str(random.randint(1, 100))
                    pay_product_ids = str(random.randint(1, 100))
                else:
                    raise Exception("action error")

                row = (date, userid, sessionid, page_id, action_time, search_key_word, click_category_id,
                       click_product_id, order_category_ids, order_product_ids, pay_category_ids, pay_product_ids, city_id)
                row = ",".join(row)
                rows.append(row)

    with open(user_visit_actions_filename, 'w') as f:
        for line in rows:
            f.write(line + "\n")

    """初始化 user_info"""
    rows.clear()
    genders = ["male", "female"]
    for i in range(1, 101):
        userid = str(i)
        username = "user" + str(i)
        name = "name" + str(i)
        age = str(random.randint(1, 60))
        professional = "professional" + str(i)
        city = "city" + str(random.randint(0, 9))
        gender = genders[random.randint(0, 1)]
        row = (userid, username, name, age, professional, city, gender)
        row = ",".join(row)
        rows.append(row)

    with open(user_info_filename, 'w') as f:
        for line in rows:
            f.write(line + "\n")


if __name__ == '__main__':
    imitate_data()









