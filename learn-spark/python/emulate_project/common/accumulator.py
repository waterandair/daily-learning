#!/usr/bin/python3
# -*- coding utf-8 -*-
from .constant import *
from pyspark import AccumulatorParam


class SessionAggrAccumulator(AccumulatorParam):

    """
    自定义累加器
    """

    def zero(self, value):
        return {
            SESSION_COUNT: 0,
            TIME_PERIOD_1s_3s: 0,
            TIME_PERIOD_4s_6s: 0,
            TIME_PERIOD_7s_9s: 0,
            TIME_PERIOD_10s_30s: 0,
            TIME_PERIOD_30s_60s: 0,
            TIME_PERIOD_1m_3m: 0,
            TIME_PERIOD_3m_10m: 0,
            TIME_PERIOD_10m_30m: 0,
            TIME_PERIOD_30m: 0,
            STEP_PERIOD_1_3: 0,
            STEP_PERIOD_4_6: 0,
            STEP_PERIOD_7_9: 0,
            STEP_PERIOD_10_30: 0,
            STEP_PERIOD_30_60: 0,
            STEP_PERIOD_60: 0
        }

    def addInPlace(self, value1, value2):
        # print(value1, value2)
        if value1 == "":
            return value2
        if isinstance(value2, dict):
            # rdd 可能会被分割成多分并行计算,所以这里处理当 value2 传入的是某个rdd某个部分计算的值
            value = {k: v + value2[k] for k, v in value1.items()}
            return value
        else:
            value1[value2] += 1
            return value1

