#!/usr/bin/ python3
# -*- coding: utf-8 -*-


class Solution:
    def removeElement(self, nums, val):
        """
        :type nums: List[int]
        :type val: int
        :rtype: int
        """
        start, end = 0, len(nums) - 1
        while start <= end:
            if nums[start] == val:
                nums[start], nums[end], end = nums[end], nums[start], end - 1
            else:
                start += 1
        print(nums[0:start])
        return start


if __name__ == '__main__':
    solution = Solution()

    nums = [4]
    nums2 = [0,1,2,2,3,0,4,2]
    val = 2
    res1 = solution.removeElement(nums2, val)
    print(res1)