package main

import "fmt"

func main() {
	// slices 比数组更常用

	s := make([]string, 3)
	fmt.Println("emp:", s)

	s[0] = "a"
	s[1] = "b"
	s[2] = "c"
	fmt.Println("set:", s)
	fmt.Println("get:", s[2])
	fmt.Println("len:", len(s), "cap:", cap(s))

	// 给 slice 添加元素
	s = append(s, "d")
	s = append(s, "e", "f")
	fmt.Println("apd:", s)

	// 复制 slice
	c := make([]string, len(s))
	copy(c, s)
	fmt.Println("cpy:", c)

	// slice 切片
	l := s[2:5]
	fmt.Println("sl1:", l)  // [c, d, e]

	l = s[:5]
	fmt.Println("sl2:", l)  // [a, b, c, d, e]

	l = s[2:]
	fmt.Println("sl3:", l)  // [c, d, e, f]

	t := []string{"g", "h", "i"}
	fmt.Println("dcl:", t)

	// 指定第一维的长度是3
	twoD := make([][]int, 3)
	for i := 0; i < 3; i++ {
		// 不同于数据，slice 的内维长度可以变化
		innerLen := i + 1
		twoD[i] = make([]int, innerLen)
		for j := 0; j < innerLen; j++ {
			twoD[i][j] = i + j
		}
	}
	fmt.Println("2d: ", twoD)  // [[0] [1 2] [2 3 4]]
}