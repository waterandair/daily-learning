#!/usr/bin/ python3
# -*- coding: utf-8 -*-

class Solution:
    def sortColors1(self, nums):
        """
        :type nums: List[int]
        :rtype: void Do not return anything, modify nums in-place instead.
        """
        count = {0: 0, 1: 0, 2: 0}
        for i in nums:
            count[i] += 1
        key = 0
        for k, v in count.items():
            for i in range(v):
                nums[key] = k
                key += 1


    def sortColors2(self, nums):
        l = -1  # [0,l]  0
        r = len(nums)  # [l,r]  2

        i = 0
        while l < r and i < r:
            if nums[i] == 0:
                l += 1
                nums[l], nums[i] = nums[i], nums[l]
                i += 1
            elif nums[i] == 1:
                i +=1

            else:
                r -= 1
                nums[i], nums[r] = nums[r], nums[i]






if __name__ == '__main__':
    solution = Solution()
    nums = [2,0,2,1,1,0]
    solution.sortColors2(nums)
    print(nums)