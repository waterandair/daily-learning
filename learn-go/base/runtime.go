package main

import (
	"fmt"
	"runtime"
)

func say(s string) {
	for i := 0; i < 5; i++ {
		runtime.Gosched()
		fmt.Println(s)
	}
}


/*
runtime包中有几个处理goroutine的函数：
Goexit			退出当前执行的goroutine，但是defer函数还会继续调用

Gosched 		让出当前goroutine的执行权限，调度器安排其他等待的任务运行，并在下次某个时候从该位置恢复执行。

NumCPU			返回 CPU 核数量

NumGoroutine	返回正在执行和排队的任务总数

GOMAXPROCS		用来设置可以并行计算的CPU核数的最大值，并返回之前的值。
*/
func main() {
	runtime.GOMAXPROCS(1)  // 单线程演示
	go say("world")  // 开一个新的 Goroutine 执行
	say("hello") // 当前 goroutines 执行

}