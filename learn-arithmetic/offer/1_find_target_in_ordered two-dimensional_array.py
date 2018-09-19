# -*- coding:utf-8 -*-
"""
题目：二维数组中的查找
描述：在一个二维数组中（每个一维数组的长度相同），每一行都按照从左到右递增的顺序排序，每一列都按照从上到下递增的顺序排序。请完成一个函数，输入这样的一个二维数组和一个整数，判断数组中是否含有该整数。
思路：描述中提到是有序数组，所以很容易想到二分查找，但其实更好的做法是从矩阵的左下角或右上角开始，通过与目标函数比较大小，可以找出一条通往目标值的唯一通道
"""


class Solution:

    def Find(self, target, array):
        rows, cols = len(array), len(array[0])
        # 找到矩阵的右上角
        x, y = 0, cols - 1
        # 从右上角开始找目标值
        while x < rows and y >= 0:
            if array[x][y] == target:
                return True
            elif array[x][y] < target:
                x += 1
            else:
                y -= 1
        return False


if __name__ == '__main__':
    arr = [
        [2, 3, 4, 5],
        [3, 4, 5, 8],
        [5, 6, 8, 10]
    ]

    solution = Solution()
    print(solution.Find(6, arr))


