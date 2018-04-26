#!/usr/bin/ python3
# -*- coding: utf-8 -*-


def sort(nums):
    for i in range(len(nums) - 1):
        for j in range(len(nums)-1 - i):
            if nums[j] > nums[j+1]:
                nums[j], nums[j+1] = nums[j+1], nums[j]


if __name__ == '__main__':

    nums = [54,26,93,17,77,31,44,55,20]
    sorted_alist = sort(nums)
    print(nums)
