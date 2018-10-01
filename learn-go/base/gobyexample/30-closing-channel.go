package main

import "fmt"

// 关闭 channel 表示不在发送任何值，这对于告知接收方已完成非常有用

func main() {
	jobs := make(chan int, 5)
	done := make(chan bool)

	go func() {
		for {
			j, more := <- jobs
			if more {
				fmt.Println("received job", j)
			} else {
				fmt.Println("received all jobs")
				done <- true
				return
			}
		}
	}()

	for j := 1; j <= 3; j++ {
		jobs <- j
		fmt.Println("send job", j)
	}
	close(jobs)
	fmt.Println("send all jobs")

	<-done
}