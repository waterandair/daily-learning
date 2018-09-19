#!/usr/bin/python3
# -*- coding：utf-8 -*-


def search(nums, n):
    """
    二分搜索（Binary search）是一项用于搜索已排序数据的技术。它通过选出数据的中项，与目标数值相比较。
    """
    l = 0
    r = len(nums) - 1

    print(__search1(nums, l, r, n))
    print(__search2(nums, l, r, n))


def __search1(nums, l, r, n):
    """
    循环实现二分查找
    """

    while l <= r:
        mid = l + (r - l) // 2
        v = nums[mid]
        if v == n:
            return mid
        elif v > n:
            r = mid - 1
        else:
            l = mid + 1

    return -1


def __search2(nums, l, r, n):
    """
    递归实现二分查找
    """
    mid = l + (r - l) // 2
    v = nums[mid]
    if l <= r:
        if v == n:
            return mid
        elif v > n:
            return __search2(nums, l, mid - 1, n)
        else:
            return __search2(nums, mid + 1, r, n)
    else:
        return -1


if __name__ == '__main__':
    nums = range(0, 20, 2)
    print(list(nums))
    search(nums, 15)