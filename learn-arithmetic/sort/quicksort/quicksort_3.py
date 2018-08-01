import random
# 三路快排


def quick_sort(nums, size):

    _quicksort(nums, 0, size-1)


def _quicksort(nums, l, r):

    if l >= r:
        return

    lt, gt = _partition(nums, l, r)
    _quicksort(nums, l, lt-1)
    _quicksort(nums, gt, r)


def _partition(nums, l, r):
    """
        三路快排，从第一个和最后一个元素同时开始找出 <= v 或 >= v 的元素
    """
    # 随机选出基准元素并与第一个元素交换
    rand_index = random.randint(l, r)
    nums[rand_index], nums[l] = nums[l], nums[rand_index]

    v = nums[l]
    lt = l
    gt = r
    i = l + 1

    while i <= gt:
        if nums[i] > v:
            nums[gt], nums[i] = nums[i], nums[gt]
            gt -= 1
        elif nums[i] < v:
            lt += 1
            nums[lt], nums[i] = nums[i], nums[lt]
            i += 1
        else:
            i += 1

    nums[l], nums[lt] = nums[lt], nums[l]

    return lt, gt


if __name__ == '__main__':
    nums = [54, 26, 93, 17, 77, 77, 77, 31, 44, 55, 20]

    quick_sort(nums, len(nums))
    print(nums)

