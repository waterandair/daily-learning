import random


def quick_sort(nums, size):

    _quick_sort(nums, 0, size-1)


def _quick_sort(nums, l, r):

    if l > r:
        return

    p = _partition(nums, l, r)

    _quick_sort(nums, l, p-1)
    _quick_sort(nums, p+1, r)


def _partition(nums, l, r):
    """
    一路快排，从第一个元素开始循环到最后一个元素
    """
    # 随机选出基准元素并与第一个元素交换
    rand_index = random.randint(l, r)
    nums[rand_index], nums[l] = nums[l], nums[rand_index]

    j = l  # 基准元素 v 当前应该在的位置
    v = nums[l]  # 基准元素 v 的值
    i = l + 1  # 从 i 循环到 r

    while i <= r:
        # 把小于基准元素的值交换到数组的左边
        if nums[i] < v:
            j += 1
            nums[j], nums[i] = nums[i], nums[j]
        i += 1

    # 最后把基准元素交换到 j 的位置
    nums[j], nums[l] = nums[l], nums[j]
    return j


if __name__ == '__main__':
    nums = [54, 26, 93, 17, 77, 31, 44, 55, 20]

    quick_sort(nums, len(nums))
    print(nums)
