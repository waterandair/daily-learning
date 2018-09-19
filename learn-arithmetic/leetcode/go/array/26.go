package main

import (
	"fmt"
	)

func removeDuplicates(nums []int) int {

	if len(nums) == 0 {
		return 0
	}
	k := 1
	for i, num := range nums{
		if i > 0 {
			if num != nums[i-1] {
				nums[k] = num
				k += 1
			}
		}
	}

	temp_nums := nums[:k]

	return len(temp_nums)
}

func main() {
	nums := []int{}
	res := removeDuplicates(nums)
	fmt.Println(res)
}
