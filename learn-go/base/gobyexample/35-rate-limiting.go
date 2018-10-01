package main

import (
	"fmt"
	"time"
)

// 限速对于控制资源利用和维护服务质量非常重要。go 可以通过 goroutine，channels和ticker优雅的实现限速
func main() {
	requests := make(chan int, 5)
	for i := 1; i <= 5; i++ {
		requests <- i
	}
	close(requests)

	// 限制器 每 200 毫秒执行一次
	limiter := time.Tick(200 * time.Millisecond)

	for req := range requests {
		<- limiter
		fmt.Println("request", req, time.Now())
	}
	fmt.Println("********************************")



	// 允许在限制器中有突发请求，但保留总体速率限制
	// 此 channel 允许最多三个事件的突发请求
	burstyLimiter := make(chan time.Time, 3)

	for i := 0; i < 3; i++ {
		burstyLimiter <- time.Now()
	}

	go func() {
		for t := range time.Tick(200 * time.Millisecond) {
			burstyLimiter <- t
		}
	}()

	burstyRequests := make(chan int, 5)
	for i := 1; i <= 5; i++ {
		burstyRequests <- i
	}
	close(burstyRequests)

	// 得益于 burstyLimiter， 前三个请求立即执行
	for req := range burstyRequests {
		<- burstyLimiter
		fmt.Println("request", req, time.Now())
	}
}
