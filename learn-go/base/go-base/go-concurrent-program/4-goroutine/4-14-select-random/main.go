package main

import "fmt"

/**
当多个case同时满足运行条件的时候，运行时系统通过一个伪随机数算法选中一个 case

下面代码的输出值每次都不一样，就是因为伪随机数

default: 可以放到 select 中的任何位置
 */
func main() {

	chanCap := 5
	intChan := make(chan int, chanCap)
	for i := 0; i < chanCap; i++ {
		select {
		case intChan <- 1:
		case intChan <- 2:
		case intChan <- 3:
		}
	}

	for i := 0; i < chanCap; i++ {
		fmt.Printf("%d\n", <-intChan)
	}
}
