package main

import "fmt"

/**
	select 中 case 右边的表达式都会先求值，顺序是从左到右，从上到下
 */

var intChan1 chan int
var intChan2 chan int
var channels = []chan int{intChan1, intChan2}
var numbers = []int{1, 2, 3, 4, 5}

func main() {
	select {
	case getChan(0) <- getNumber(0):
		fmt.Println("1th case is selected")
	case getChan(1) <- getNumber(1):
		fmt.Println("the 2nd case is selected")
	default:
		fmt.Println("default")
	}
}

//channels [0]
//numbers[0]
//channels [1]
//numbers[1]
//default

// 从打印中可以看出，select case 中的表达式是从左到右，从上到下一次执行的

func getNumber(i int) int {
	fmt.Printf("numbers[%d]\n", i)
	return numbers[i]
}

func getChan(i int) chan int {
	fmt.Printf("channels [%d]\n", i)
	return channels[i]
}
