package main

import "fmt"

/**
在实际使用中，常常把select语句梵高一个单独的 goroutine 中去执行，这样即使 select 阻塞了，也不会造成死锁。

select 语句也常常与 for 语句联用，以便持续操作通道

使用内建函数 cap 轻松判断 channel 是否有缓冲
 */
func main() {
	intChan := make(chan int, 10)
	for i := 0; i < 10; i++ {
		intChan <- i
	}
	close(intChan)

	syncChan := make(chan struct{}, 1)

	go func() {
	Loop:
		for {
			select {
			case e, ok := <- intChan:
				if !ok {
					fmt.Println("End.")
					break Loop
				}
				fmt.Printf("received: %v\n", e)
			}
		}
	syncChan <- struct{}{}
	}()

	<-syncChan
}
