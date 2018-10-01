package main

import (
	"fmt"
	"time"
)

// 这个 worker 运行几个实例，这些 worker 从 jobs channel 中接收 worker， 发送响应结果给 results channel
// 每个任务会 sleep 一秒钟，用于模拟耗时任务
func worker2(id int, jobs <-chan int, results chan<- int) {
	for j := range jobs {
		fmt.Println("worker", id, "started job", j)
		time.Sleep(time.Second)
		fmt.Println("worker", id, "finished job", j)
		results <- j*2
	}
}

// 使用 goroutine 和 channel 实现一个工作池
func main() {
	jobs := make(chan int, 100)
	results := make(chan int, 100)

	// 启动三个worker， 初始是阻塞的
	for work := 1; work <= 3; work++ {
		go worker2(work, jobs, results)
	}

	// 发送 5 个 job
	for j := 1; j <= 5; j++ {
		jobs <- j
	}
	close(jobs)  // 注意close

	// 接收所有 jobs 的结果
	for a := 1; a <= 5; a++ {
		<-results
	}

	// 5 个 job 总耗时 2 秒左右， 因为有 3 个 worker 并发执行
}
