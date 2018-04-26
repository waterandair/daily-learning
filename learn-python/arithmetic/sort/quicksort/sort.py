#!/usr/bin/ python3
# -*- coding: utf-8 -*-


def quick_sort(nums, start, end):

    if start >= end:
        return

    mid = _partition(nums, start, end)
    quick_sort(nums, 0, mid)
    quick_sort(nums, mid+1, end)



def _partition(nums, start, end):

    mid = nums[start]
    pos = 0

    for i in range(start+1, end+1):
        if nums[i] < mid:
            pos += 1
            nums[start+pos], nums[i] = nums[i], nums[start+pos]

    nums[start], nums[start+pos] = nums[start+pos], nums[start]
    return start+pos


if __name__ == '__main__':
    nums = [54,26,93,17,77,31,44,55,20]

    quick_sort(nums, 0, 8)
    print(nums)


