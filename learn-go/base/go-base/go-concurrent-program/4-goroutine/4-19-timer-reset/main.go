package main

import (
	"fmt"
	"time"
)

/**
timer 定时器是可以复用的

使用 timer 应该注意：
	尽量复用
	从 已停止的 timer C 获取值，会永远阻塞
	复用前应该确保 C 中的值已经被取出，如果有值的话，重置并不能清除
 */
func main() {
	intChan := make(chan int, 1)

	go func() {
		for i := 0; i < 5; i++ {
			time.Sleep(time.Second)
			intChan <- i
		}
		close(intChan)
	}()

	timeout := time.Millisecond * 500

	var timer *time.Timer

	for {

		// 重置 timer
		if timer == nil {
			timer = time.NewTimer(timeout)
		} else {
			timer.Reset(timeout)
		}

		select {
		case e, ok := <-intChan:
			if !ok {
				fmt.Print("end")
			}
			fmt.Printf("received: %v\n", e)
		case <-timer.C:
			fmt.Println("timeout")
		}



	}


}
