#!/usr/bin/ python3
# -*- coding: utf-8 -*-

import time
import random
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers=[
        "127.0.0.1:9092"
    ],
    batch_size=5,
    linger_ms=1000
)
# key 用于hash， 相同 key 的 value 提交到相同的 partition，key 的值默认为 None， 表示随机分配
while True:
    timestamp = round(time.time())
    province_city = {'内蒙古': ['乌海', '呼市', '包头'], '北京': ['北京'], '湖北': ['武汉', '宜昌', '随州']}
    province = random.choice(list(province_city.keys()))
    city = random.choice(province_city[province])
    user_id = random.randint(1, 1000)
    adid = random.randint(1, 10)
    row = [str(timestamp), province, city, str(user_id), str(adid)]
    mes = " ".join(row).encode()
    producer.send(topic='ad_click', value=mes, key=None)
    # 随机休眠 100ms ～ 500ms
    time.sleep(round(random.uniform(0.1, 0.5), 1))
