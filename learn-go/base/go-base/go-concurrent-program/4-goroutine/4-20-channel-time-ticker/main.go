package main

import (
	"fmt"
	"time"
)

// 断续器可以理解为 crontab

/**
	断续器的通知也是用 channel， 并且字段和 timer 名称一样， 也是 C
 */
func main() {
	intChan := make(chan int, 1)
	ticker := time.NewTicker(time.Second)

	go func() {
		for _ = range ticker.C {
			select {
			case intChan <- 1:
			case intChan <- 2:
			case intChan <- 3:
			}
		}
		fmt.Println("end. [sender]")
	}()

	var sum int
	for e := range intChan {
		fmt.Printf("received: %v\n", e)
		sum += e
		if sum > 10 {
			fmt.Printf("get: %v\n", sum)
			break
		}
	}
	fmt.Println("end. [received]")
}
