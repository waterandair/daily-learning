#!/usr/bin/ python3
# -*- coding: utf-8 -*-


def sort(nums):
    """
    插入排序，
    :param nums:
    :return:
    """
    size = len(nums)
    for i in range(1, size):
        for j in range(i, 0, -1):
            if nums[j] < nums[j-1]:
                nums[j], nums[j-1] = nums[j-1], nums[j]


def sort2(nums):
    """
    优化，减少交换操作
    :param nums:
    :return:
    """
    size = len(nums)
    for i in range(1, size):
        temp = nums[i]
        index = i
        while nums[index-1] > temp and index > 0:
            nums[index] = nums[index-1]
            index -= 1

        nums[index] = temp


if __name__ == '__main__':
    alist = [54, 226, 93, 17, 77, 31, 44, 55, 20]
    sort2(alist)
    print(alist)
