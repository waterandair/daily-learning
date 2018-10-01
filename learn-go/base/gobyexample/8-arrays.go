package main

import "fmt"

func main() {
	// array 不可变
	var a [5]int
	fmt.Println("emp:", a)

	a[4] = 100
	fmt.Println("set:", a )
	fmt.Println("get", a[4])

	fmt.Println("len:", len(a))

	// 初始化数组
	b := [5]int{1, 2, 3, 4, 5}
	fmt.Println("dcl:", b)


	// 二维数组
	var twoD [2][3]int
	for i := 0; i < 2; i++ {
		for j := 0; j < 3; j++ {
			twoD[i][j] = i + j
		}
	}

	fmt.Println("2d: ", twoD)  // [[0 1 2] [1 2 3]]
}