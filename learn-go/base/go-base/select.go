package main

import (
	"fmt"
	"time"
)

/*
select()
	早在Unix时代, select 机制就已经被引入。
	通过调用 select() 函数来监控一系列的文件句柄,一旦其中一个文件句柄发生了IO动作,该 select() 调用就会被返回。
	后来该机制也被用于实现高并发的Socket服务器程序。
	Go语言直接在语言级别支持 select 关键字,用于处理异步IO问题

	select默认是阻塞的，只有当监听的 channel 中有发送或接收可以进行时才会运行，当多个channel都准备好的时候，select是随机的选择一个执行的。

select 用法类似 switch
	select 限制每个 case 语句里必须是一个IO操作
	default就是当监听的channel都没有准备好的时候，默认执行的（select不再阻塞等待channel）。

select{} 可以用于阻塞一个 goroutine

*/
func main() {
	c := make(chan int)
	quit := make(chan int)

	go func() {
		for i := 0; i < 10; i++ {
			fmt.Println(<-c)
		}
		quit <- 0
	}()

	fibonacci_(c, quit)

	timeout()
}


func fibonacci_(c, quit chan int) {
	x, y := 1, 1
	for {
		select {
			case c <- x:
				x, y = y, x + y
			case <- quit:
				fmt.Println("quit")
				return
		}
	}
}

// 超时机制
func timeout() {
	c := make(chan int)
	o := make(chan bool)

	go func() {
		for {
			select {
			case v := <- c:
				fmt.Println(v)
			case <- time.After(3 * time.Second):
				fmt.Println("timeout")
				o <- true
				break
			}
		}

	}()

	// 这里阻塞直到超时，没有超时的时候会持续从 c 中读取值
	<- o
}

func timeout2() {
	ch := make(chan int)
	timeout := make(chan bool, 1)
	go func() {
		time.Sleep(3 * time.Second)
		timeout <- true
	}()

	select {
		case <-ch:
			// 从 ch 中读取数据
		case <-timeout:
			// 到了超时时间还没有从ch 中取到数据，就会从 timeout中取到，并退出
	}

}


