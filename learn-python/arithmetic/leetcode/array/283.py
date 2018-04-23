#!/usr/bin/ python3
# -*- coding: utf-8 -*-


class Solution:

    def move_zeroes1(self, nums):

        k = 0
        for i in range(0,len(nums)):
            if nums[i] != 0:
                nums[k] = nums[i]
                k += 1
        for i in range(k, len(nums)):
            nums[i] = 0
        return nums

    def move_zoroes2(self, nums):
        k = 0
        for i in range(0, len(nums)):
            if nums[i] != 0:
                if i != k:
                    nums[k], nums[i] = nums[i], nums[k]
                k += 1
        return nums


if __name__ == '__main__':
    nums = [0, 1, 0, 3, 12]
    solution = Solution()
    print(solution.move_zeroes1(nums))
    print(solution.move_zoroes2(nums))