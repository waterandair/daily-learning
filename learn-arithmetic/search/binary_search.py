#!/usr/bin/python3
# -*- coding：utf-8 -*-


def binary_search1(alist, item):
    """
    二分查找，循环
    :param alist:
    :param item:
    :return:
    """
    left = 0
    right = len(alist) - 1

    while left <= right:

        mid = (left + right) // 2
        if alist[mid] == item:
            return mid
        else:
            if item < alist[mid]:
                right = mid - 1
            else:
                left = mid + 1

    return -1


def binary_search2(alist, item):
    """
    递归
    二分法搜索（Binary search）是一项用于搜索已排序数据的技术。它通过选出数据的中项，与目标数值相比较。
    :param alist:
    :param item:
    :return:
    """
    size = len(alist)
    if size == 0:
        return False
    else:
        mid = size // 2
        if item == alist[mid]:
            return True
        else:
            if item < alist[mid]:
                return binary_search2(alist[: mid], item)
            else:
                return binary_search2(alist[mid+1:], item)


if __name__ == '__main__':
    alist = range(0, 1000000000, 2)
    res1 = binary_search1(alist, 16)
    res2 = binary_search2(alist, 16)
    print(res1, res2)