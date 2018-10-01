package main

import (
	"fmt"
	"sort"
)

// 对一些集合进行自定义排序

// 对 string 类型的数据根据长度排序而不是字母顺序
type byLength []string

// 实现 sort.Interface 的方法接口
// 计算长度
func (s byLength) Len() int {
	return len(s)
}

// 交换位置
func (s byLength) Swap(i, j int) {
	s[i], s[j] = s[j], s[i]
}

// 比较长短
func (s byLength) Less(i, j int) bool {
	return len(s[i]) < len(s[j])
}

func main() {
	fruits := []string{"peach", "banana", "kiwi"}
	sort.Sort(byLength(fruits))
	fmt.Println(fruits)
}


