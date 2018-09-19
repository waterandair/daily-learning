package main

func removeElement(nums []int, val int) int {
	l, r := 0, len(nums)
	for l < r {
		if nums[l] == val {
			r --
			nums[l], nums[r] = nums[r], nums[l]
		} else {
			l ++
		}
	}

	return len(nums[:r])
}
