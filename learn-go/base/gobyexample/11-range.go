package main

import "fmt"

func main() {
	// range 用于迭代各种数据结构

	nums := []int{1, 2, 3}
	sum := 0
	for _, num := range nums {
		sum += num
	}
	fmt.Println(sum)

	// range 返回的第一个变量表示索引
	for i, num := range nums {
		if num == 2 {
			fmt.Println("index:", i)
		}
	}

	// 迭代 map
	kvs := map[string]string{"a": "apple", "b": "banana"}
	// 注意 map 是无序的
	for k, v := range kvs {
		fmt.Printf("%s -> %s\n", k, v)
	}

	// 只迭代 key
	for k := range kvs {
		fmt.Println("keyL:", k)
	}

	// 遍历字符串时， 第一个变量是索引，第二个是字符的 Unicode 码
	for i, c := range "go" {
		fmt.Println(i, c)
	}
}