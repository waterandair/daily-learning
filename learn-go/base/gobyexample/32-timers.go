package main

import (
	"fmt"
	"time"
)

// Timer 是在未来某个时刻执行一次指定代码，Ticker 是每隔一段时间重复执行某段代码
func main() {
	// 创建一个 2 秒的定时器，到点后，会使用 channel 通知
	timer1 := time.NewTimer(2 * time.Second)

	<- timer1.C
	fmt.Println("timer 1 expired")

	timer2 := time.NewTimer(time.Second)
	go func() {
		<- timer2.C
		fmt.Println("Timer 2 expired")
	}()

	// 单纯的等待功能可以使用 time.Sleep() 完成
	// 选择 Timer 的理由是它可以在中止等待
	stop2 := timer2.Stop()
	if stop2 {
		fmt.Println("timer 2 stopped")
	}
}
