#!/usr/bin/ python3
# -*- coding: utf-8 -*-


def sort(nums):
    for i in range(len(nums) - 1):
        for j in range(len(nums)-1 - i):
            if nums[j] > nums[j+1]:
                nums[j], nums[j+1] = nums[j+1], nums[j]


def sort2(nums):
    exchange = False
    for i in range(len(nums)-1, 0, -1):
        for j in range(i):
            if nums[j] > nums[j+1]:
                nums[j], nums[j+1] = nums[j+1], nums[j]
                exchange = True
        if not exchange:
            break


if __name__ == '__main__':

    nums = [54, 26, 93, 17, 77, 31, 44, 55, 20]
    # nums = [1, 2, 3, 4, 5, 6]
    sorted_alist = sort2(nums)
    print(nums)
