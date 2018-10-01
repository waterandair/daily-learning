package main

import (
	"fmt"
)

func sum(nums ...int) {
	fmt.Println(nums)
	total := 0
	for _, num := range nums {
		total += num
	}

	fmt.Println(total)
}
func main() {
	sum(1, 2)
	sum(1, 2, 3)

	// slice 后加 ... 可以转换为 多变量类型
	nums := []int{1, 2, 3, 4}
	sum(nums...)

}
