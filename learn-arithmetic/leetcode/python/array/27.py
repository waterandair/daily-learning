#!/usr/bin/ python3
# -*- coding: utf-8 -*-


class Solution:
    """
    27. Given an array nums and a value val, remove all instances of that value in-place and return the new length.

        Do not allocate extra space for another array, you must do this by modifying the input array in-place with O(1) extra memory.

        The order of elements can be changed. It doesn't matter what you leave beyond the new length.
    """
    def removeElement(self, nums, val):
        l, r = 0, len(nums)
        while l < r:
            if nums[l] == val:
                r -= 1
                nums[l], nums[r] = nums[r], nums[l]
            else:
                l += 1
        return len(nums[0:r])


if __name__ == '__main__':
    solution = Solution()

    nums = [4]
    nums2 = [0,1,2,2,3,0,4,2]
    val = 2
    res1 = solution.removeElement(nums2, val)
    print(res1)