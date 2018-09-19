#!/usr/bin/ python3
# -*- coding: utf-8 -*-


class Solution:
    def removeDuplicates(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        k = 1
        if len(nums) > 1:
            while k != len(nums):
                if nums[k] == nums[k-1]:
                    nums.pop(k)
                    k -= 1
                k += 1

        return len(nums)


    def removeDuplicates2(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        k = 1
        for i in range(len(nums)):
            if i > 0:
                if nums[i] != nums[i-1]:
                    nums[k] = nums[i]
                    k += 1

        temp_nums = nums[:k]

        return len(temp_nums)


    def removeDuplicates3(self, nums):

        l = 0
        i = 1
        r = len(nums) - 1
        while i <= r:
            if nums[i] != nums[l]:
                l += 1
                if i != l:
                    nums[l] = nums[i]
            i += 1

        return len(nums[:l+1])


if __name__ == '__main__':
    solution = Solution()
    nums = [0, 0, 1, 1, 1, 2, 2, 3, 3, 4]
    print(solution.removeDuplicates(nums))
    print(solution.removeDuplicates3(nums))  # 速度更快
