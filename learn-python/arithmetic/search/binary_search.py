#!/usr/bin/python3
#-*- coding utf-8 -*-

def binary_search(alist, item):
    """
    二分法搜索（Binary search）是一项用于搜索已排序数据的技术。它通过选出数据的中项，与目标数值相比较。
    :param list:
    :param item:
    :return:
    """
    alist_len = len(alist)
    if alist_len <= 0:
        return False
    else:
        mid = alist_len // 2
        if alist[mid] == item:
            return True
        else:
            if item < alist[mid]:
                return binary_search(alist[:mid], item)
            else:
                return binary_search(alist[mid + 1:], item)

