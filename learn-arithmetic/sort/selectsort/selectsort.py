#!/usr/bin/ python3
# -*- coding: utf-8 -*-


def select_sort(arr, size):
    """选择排序，每个元素与他后面最小的元素交换位置"""
    for i in range(size - 1):      # 最后一个元素不需要再遍历
        min_index = i
        for j in range(i+1, size):
            if arr[j] < arr[min_index]:  # 找出最小的元素
                min_index = j
        arr[i], arr[min_index] = arr[min_index], arr[i]  # 将当前位置与最小元素交换


def advance_select_sort(arr, size):
    """优化选择排序,在每一轮排序中,找出当前未处理元素的最大值和最小值"""
    for i in range(size - 1):
        left = min_index = i
        right = max_index = size - 1 - i

        if left >= right:
            return

        if arr[left] > arr[right]:  # 每次遍历要先保证左边的值大于右边的值
            arr[left], arr[right] = arr[left], arr[right]

        for j in range(left + 1, right):
            if arr[j] < arr[min_index]:  # 找出最小值
                min_index = j
            if arr[j] > arr[max_index]:  # 找出最大值
                max_index = j

        arr[left], arr[min_index] = arr[min_index], arr[left]  # 未排序元素中的最小值与未排序的最左端交换
        arr[right], arr[max_index] = arr[max_index], arr[right]  # 未排序元素中的最大值与未排序的最右端交换


if __name__ == '__main__':
    arr = [54, 226, 93, 17, 77, 31, 44, 55, 20]
    select_sort(arr, len(arr))
    print(arr)

    arr = [54, 226, 93, 17, 77, 31, 44, 55, 20]
    advance_select_sort(arr, len(arr))
    print(arr)


