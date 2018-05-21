package main

import "time"

// select默认是阻塞的，只有当监听的channel中有发送或接收可以进行时才会运行，当多个channel都准备好的时候，select是随机的选择一个执行的。
// 在select里面还有default语法，select其实就是类似switch的功能，default就是当监听的channel都没有准备好的时候，默认执行的（select不再阻塞等待channel）。

func fibonacci(c, quit chan int) {
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

	<- o
}

func main() {
	c := make(chan int)
	quit := make(chan int)

	go func() {
		for i := 0; i < 10; i++ {
			fmt.Println(<-c)
		}
		quit <- 0
	}()

	fibonacci(c, quit)

	timeout()
}
