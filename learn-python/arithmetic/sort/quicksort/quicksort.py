#!/usr/bin/python3
#-*- coding utf-8 -*-

"""
快速排序（英语：Quicksort），又称划分交换排序（partition-exchange sort），通过一趟排序将要排序的数据分割成独立的两部分，其中一部分的所有
数据都比另外一部分的所有数据都要小，然后再按此方法对这两部分数据分别进行快速排序，整个排序过程可以递归进行，以此达到整个数据变成有序序列。

步骤为：

1. 从数列中挑出一个元素，称为"基准"（pivot），
2. 重新排序数列，所有元素比基准值小的摆放在基准前面，所有元素比基准值大的摆在基准的后面（相同的数可以到任一边）。在这个分区结束之后，该基准就处
   于数列的中间位置。这个称为分区（partition）操作。
3. 递归地（recursive）把小于基准值元素的子数列和大于基准值元素的子数列排序。
"""

def quick_sort(alist, start, end):
    """
    快速排序
    :param alist:
    :param start:
    :param end:
    :return:
    """

    # 递归的退出条件
    if start >= end:
        return

    # 设定起始元素为要寻找的基准元素
    mid = alist[start]

    # low 为序列左边的由左向右移动的游标
    low = start

    # hign 为序列右边的由右向左移动的游标
    high = end

    while low < high:
        # 如果 low 与 high 未重合,high指向的元素不比基准元素小,则high向左移动
        while low < high and alist[high] >= mid:
            high -= 1

        # 将 high 指向的元素放到 low 的位置上
        alist[low] = alist[high]

        # 如果 low 与 high 未重合,low 指向的元素不比基准元素小,则 high 向左移动
        while low < high and alist[low] < mid:
            low += 1

        # 将 low 指向的元素放到 high 的位置上
        alist[high] = alist[low]

    # 退出循环后,low 与 high 重合,此时所指位置为基准元素的正确位置
    # 将基准元素放到该位置
    alist[low] = mid

    # 对基准元素左边的子序列进行快速排序
    quick_sort(alist, start, low - 1)

    # 对基准元素右边的子序列进行快速排序
    quick_sort(alist, low + 1, end)






































