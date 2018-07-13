#!/usr/bin/ python3
# -*- coding: utf-8 -*-


class Solution:
    def removeDuplicates(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        size = len(nums)
        i = 2
        if size < 2:
            return size
        else:
            while i < size:
                if nums[i] == nums[i-2]:
                    nums.pop(i)
                    size -= 1
                else:
                    i += 1
        return size

    def removeDuplicates2(self, nums):
        i = 0
        for n in nums:
            if i < 2 or n > nums[i - 2]:
                nums[i] = n
                i += 1
        print(nums)
        return i


if __name__ == '__main__':
    solution = Solution()
    nums = [1, 1, 1, 2, 3, 3, 3, 3, 3]
    res = solution.removeDuplicates2(nums)
    print(res)
