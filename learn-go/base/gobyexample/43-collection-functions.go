package main

import (
	"fmt"
	"strings"
)

// 返回目标 t 在 vs 中的第一个索引，没有就返回 -1
func Index(vs []string, t string) int {
	for i, v := range vs {
		if v == t {
			return i
		}
	}
	return -1
}

// 判断vs 中是否包含 t
func Include(vs []string, t string) bool {
	return Index(vs, t) >= 0
}

// 判断 vs 中是否有符合 f 的元素
func Any(vs []string, f func(string) bool) bool {
	for _, v := range vs {
		if f(v) {
			return true
		}
	}

	return false
}


// 判断 vs 中的每个元素是否都符合 f
func All(vs []string, f func(s string) bool) bool {
	for _, v := range vs {
		if !f(v) {
			return false
		}
	}

	return true
}

// 过滤
func Filter(vs []string, f func(string) bool) []string {
	vsf := make([]string, 0)
	for _, v := range vs {
		if f(v) {
			vsf = append(vsf, v)
		}
	}
	return vsf
}

// map 操作
func Map(vs []string, f func(string) string) []string {
	vsm := make([]string, len(vs))
	for i, v := range vs {
		vsm[i] = f(v)
	}
	return vsm
}

func main() {
	var strs = []string{"peach", "apple", "pear", "plum"}
	fmt.Println(Index(strs, "pear"))
	fmt.Println(Include(strs, "grape"))
	fmt.Println(Any(strs, func(v string) bool {
		return strings.HasPrefix(v, "p")
	}))
	fmt.Println(All(strs, func(v string) bool {
		return strings.HasPrefix(v, "p")
	}))
	fmt.Println(Filter(strs, func(v string) bool {
		return strings.Contains(v, "e")
	}))

	fmt.Println(Map(strs, strings.ToUpper))
}



