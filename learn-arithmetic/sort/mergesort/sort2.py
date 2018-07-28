
def sort(nums):

    __merge_sort(nums, 0, len(nums) - 1)


def __merge_sort(nums, l, r):

    if l >= r:
        return

    mid = (l+r) // 2
    __merge_sort(nums, l, mid)
    __merge_sort(nums, mid + 1, r)
    if nums[mid + 1] < nums[mid]:
        merge(nums, l, mid, r)


def merge(nums, l, mid, r):
    temp = nums[l:r+1]
    j, k = l, mid + 1
    for n in range(l, r + 1):
        if j > mid:
            nums[n] = temp[k-l]
            k += 1
        elif k > r:
            nums[n] = temp[j-l]
            j += 1

        elif temp[j-l] < temp[k-l]:
            nums[n] = temp[j-l]
            j += 1
        else:
            nums[n] = temp[k-l]
            k += 1


if __name__ == '__main__':
    nums = [6,2,3,1,5,7,4]
    sort(nums)
    print(nums)