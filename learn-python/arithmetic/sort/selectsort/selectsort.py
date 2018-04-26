#!/usr/bin/ python3
# -*- coding: utf-8 -*-


def sort(alist):
    """
    选择排序，每个元素与他后面最小的元素交换位置
    :param alist:
    :return:
    """
    size = len(alist)
    for i in range(size - 1):
        min_index = i
        for j in range(i+1, size):
            if alist[j] < alist[min_index]:
                min_index = j

        alist[i], alist[min_index] = alist[min_index], alist[i]


if __name__ == '__main__':
    alist = [54, 226, 93, 17, 77, 31, 44, 55, 20]
    sort(alist)
    print(alist)
