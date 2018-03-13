#!/usr/bin/python3
# -*- coding: utf-8 -*-
# timedelta 用于对时间进行加减计算
# class datetime.timedelta([days[, seconds[, microseconds[, milliseconds[, minutes[, hours[, weeks]]]]]]])
from datetime import datetime, timedelta, timezone

now = datetime.now()
print('now:', now)
print("type(now):", type(now))

# 用指定日期时间创建 datetime
dt = datetime(2017, 11, 2, 10, 22)
print('dt = ', dt)

# 把 datetime 转换为 timestamp
print('dt(datetime) -> timestamp:', dt.timestamp())

# 把 timestamp 转换为 datetime
t = dt.timestamp()
print('timestamp -> datetime:', datetime.fromtimestamp(t))
print('timestamp -> datetime as UTC+0', datetime.utcfromtimestamp(t))

# 从 str 读取 datetime
day = datetime.strptime('2017-11-2 10:59:55', "%Y-%m-%d %H:%M:%S")
print(type(day))  # <class 'datetime.datetime'>

# 把 datetime 格式化输出
# %y 两位数的年份表示（00-99）
# %Y 四位数的年份表示（000-9999）
# %m 月份（01-12_concurrency）
# %d 月内中的一天（0-31）
# %H 24小时制小时数（0-23）
# %I 12小时制小时数（01-12_concurrency）
# %M 分钟数（00=59）
# %S 秒（00-59）
# %a 本地简化星期名称
# %A 本地完整星期名称
# %b 本地简化的月份名称
# %B 本地完整的月份名称
# %c 本地相应的日期表示和时间表示
# %j 年内的一天（001-366）
# %p 本地A.M.或P.M.的等价符
# %U 一年中的星期数（00-53）星期天为星期的开始
# %w 星期（0-6），星期天为星期的开始
# %W 一年中的星期数（00-53）星期一为星期的开始
# %x 本地相应的日期表示
# %X 本地相应的时间表示
# %Z 当前时区的名称
# %% %号本身
print (day.strftime("'%a, %b %d %H:%M'"))

# 对日期进行加减:
print('current datetime =', day)
print('current + 10 hours =', day + timedelta(hours=10))
print('current - 1 day =', day - timedelta(days=1))
print('current + 2.5 days =', day + timedelta(days=2, hours=12))

# 把时间从UTC+0时区转换为UTC+8:
utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc)
print(timezone.utc)  # UTC+00:00
utc8_dt = utc_dt.astimezone(timezone(timedelta(hours=8)))
print('UTC+0:00 now =', utc_dt)
print('UTC+8:00 now =', utc8_dt)


