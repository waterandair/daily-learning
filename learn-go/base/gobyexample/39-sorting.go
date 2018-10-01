package main

import (
	"fmt"
	"sort"
)

// go 的 sort 包实现了内置和自定义两种类型，这里先看内置的

func main() {
	// 排序是修改当前slice，不会返回新的slice
	strs := []string{"c", "a", "b"}
	sort.Strings(strs)
	fmt.Println("Strings:", strs)

	ints := []int{7, 2, 4}
	sort.Ints(ints)
	fmt.Println("Ints: ", ints)

	// 判断是否已经排好序
	s := sort.IntsAreSorted(ints)
	fmt.Println("sorted: ", s)
}