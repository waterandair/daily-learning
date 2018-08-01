import random
# quick_sort_1 的做法，没有考虑到有大量重复元素的情况，如果有大量重复元素，都会被分配到一个partition中
# quick_sort_2 会把重复的元素平均分配到 两个 partition 中


def quick_sort(nums, size):

    _quick_sort(nums, 0, size-1)


def _quick_sort(nums, l, r):

    if l >= r:
        return

    p = _partition(nums, l, r)

    _quick_sort(nums, l, p-1)
    _quick_sort(nums, p+1, r)


def _partition(nums, l, r):
    """
    双路快排，从第一个和最后一个元素同时开始找出 <= v 或 >= v 的元素
    """
    # 随机选出基准元素并与第一个元素交换
    rand_index = random.randint(l, r)
    nums[rand_index], nums[l] = nums[l], nums[rand_index]

    v = nums[l]  # 基准元素 v 的值
    i = l + 1  # 从 i 循环到 r
    j = r

    while True:
        # 从左到右遇到小于 v 的就给 i 加 1， 假设这列数组是完全倒序的， i 最大值就是 r
        while i <= r and nums[i] < v:
            i += 1
        # 从右到左遇到大于 v 的就给 j 减 1， 假设这列数组是完全正序的， j 最小值就是 l + 1
        while j >= l + 1 and nums[j] > v:
            j -= 1

        if i > j:
            break

        # 将 >= v 的与 <= v 的数交换，并给 i 加 1， 给 j 减 1
        nums[i], nums[j] = nums[j], nums[i]
        i += 1
        j -= 1

    nums[l], nums[j] = nums[j], nums[l]
    return j


if __name__ == '__main__':
    nums = [54, 26, 93, 17, 77, 77, 77, 31, 44, 55, 20]

    quick_sort(nums, len(nums))
    print(nums)
