package main

import (
	"math"
	"sync"
	"runtime"
	"fmt"
	"os"
	"math/rand"
	"time"
)

// 并发
// Go 在语言层面对并发编程提供支持,一种类似协程,称作 goroutine 的机制。
// 只需在函数调用语句前添加 go 关键字,就可创建并发执行单元。开发人员无需了解任何
// 执行细节,调度器会自动将其安排到合适的系统线程上执行。goroutine 是一种非常轻量
// 级的实现,可在单个进程里执行成千上万的并发任务。

// 事实上,入口函数 main 就以 goroutine 运行
// 调度器不能保证多个 goroutine 执行次序,且进程退出时不会等待它们结束
// 默认情况下,进程启动后仅允许一个系统线程服务于 goroutine。可使用环境变量或标准
// 库函数 runtime.GOMAXPROCS 修改,让调度器用多个线程实现多核并行,而而不仅是并发。

func main() {
	// test_7_1()
	// test_7_2()
	// test_7_3()

	// channel
	// test_7_4()

	// test_7_5()
	// 单向
	// test_7_6()
	// select
	test_7_7()
}
func sum3(id int) {
	var x int64
	for i := 0; i < math.MaxUint32; i++ {
		x += int64(i)
	}

	println(id, x)
}

func test_7_1() {
	wg := new(sync.WaitGroup)
	wg.Add(2)

	for i:= 0; i < 2; i++ {
		go func(id int) {
			defer wg.Done()
			sum3(id)
		}(i)
	}

	wg.Wait()
	// 单线程测试 go build -o test learn-note-7.go , 执行 time -p ./test命令
	// 1 9223372030412324865
	// 0 9223372030412324865
	// real 3.03  // 程序开始到结束时间差 (非 CPU 时间)
	// user 6.05  // 用户态所使用 CPU 时间片 (多核累加)
	// sys 0.00   // 内核态所使用 CPU 时间片

	// 多线程测试
	// GOMAXPROCS=2 time -p ./test
	// 0 9223372030412324865
	// 1 9223372030412324865
	// real 3.00
	// user 5.98
	// sys 0.00
}

// 调用 runtime.Goexit 将立即终止当前 goroutine 执行,调度器确保所有已注册 defer 延迟调用被执行。
func test_7_2() {
	wg := new(sync.WaitGroup)
	wg.Add(1)

	go func() {
		defer wg.Done()
		defer println("A.defer")

		func () {
			defer println("B.defer")
			runtime.Goexit()    // 终止止当前 goroutine
			println("B")   // 不会执行
		}()

		println("A") // 不会执行
	}()

	wg.Wait()
}

// 和协程 yield 作用类似,Gosched 让出底层线程,将当前 goroutine 暂停,放回队列等待下次被调度执行。
func test_7_3() {
	runtime.GOMAXPROCS(1)
	wg := new(sync.WaitGroup)
	wg.Add(2)

	go func() {
		defer wg.Done()
		println("hello world")
	}()

	go func() {
		defer wg.Done()

		for i := 0; i < 6; i++ {
			println(i)
			if i == 3 { runtime.Gosched() }
		}
	}()
	//0
	//1
	//2
	//3
	//hello world
	//4
	//5

	wg.Wait()
}


// channel
// 引用类型 channel 是 CSP 模式的具体实现,用于多个 goroutine 通讯。其内部实现了同步,确保并发安全。
// 默认为同步模式,需要发送和接收配对。否则会被阻塞,直到另一方准备好后被唤醒。
func test_7_4() {
	data := make(chan int)   // 数据交换队列
	exit := make(chan bool)  // 退出通知

	go func() {
		for d := range data {
			fmt.Println(d)
		}

		fmt.Println("recv over")
		exit <- true  // 发出退出通知
	}()

	data <- 1
	data <- 2
	data <- 3
	close(data)  // 关闭队列

	fmt.Println("send over")
	<- exit  // 等待退出通知
}

// 异步方式通过判断缓冲区来决定是否阻塞。如果缓冲区已满,发送被阻塞;缓冲区为空, 接收被阻塞。
// 通常情况下,异步 channel 可减少排队阻塞,具备更高的效率。但应该考虑使用指针规避大对象拷⻉,将多个元素打包,减小缓冲区大小等。


func test_7_5() {
	data := make(chan int, 3)  // 缓冲区可以存储 3 个元素
	exit := make(chan bool)

	data <- 1  // 缓冲区未满前,发送不会阻塞
	data <- 2
	data <- 3

	go func() {
		// 缓冲区为空前,不会阻塞
		for d := range data {
			fmt.Println(d)
		}

		exit <- true
	}()

	data <- 4 // 如果缓冲区已满,阻塞。
	data <- 5
	close(data)

	<-exit
}

// 单向
// 可以将 channel 隐式转换为单向队列,只收或只发。
func test_7_6() {
	c := make(chan int, 3)

	var send chan<- int = c  // 只发
	var recv <-chan int = c  // 只收

	send <- 1  // 只发
	<- recv	   // 只收
}

// 选择
// 如果需要同时处理多个 channel,可使用 select 语句。它随机选择一个可用 channel 做收发操作,或执行 default case。
func test_7_7() {
	a, b := make(chan int, 3), make(chan int)

	go func() {
		v, ok, s := 0, false, ""

		for {
			// 在循环中使用 select default case 需要小心,避免形成洪水。
			select {
			case v, ok = <-a:
				s = "a"
			case v,ok = <-b:
				s = "b"
			}

			if ok {
				fmt.Println(s, v)
			} else {
				os.Exit(0)
			}
		}
	}()

	// 随机选择可用 channel 发送数据
	for i :=0; i < 5; i++ {
		select {
		case a <- i:
		case b <- i:
		}
	}

	close(a)
	select {}  // 没有可用 channel,阻塞 main goroutine。
}

// 模式
// 用简单工厂模式打包并发任务和 channel
func NewTest() chan int {
	c := make(chan int)
	rand.Seed(time.Now().UnixNano())

	go func() {
		time.Sleep(time.Second)
		c <- rand.Int()
	}()

	return c
}

// 用channel 实现信号量(semaphore)
func test_7_8() {
	wg := sync.WaitGroup{}
	wg.Add(3)

	sem := make(chan int, 1)
	for i:=0; i < 3; i++ {
		go func(id int) {
			defer wg.Done()
			sem <- 1  // 向 sem 发送数据,阻塞或者成功。

			for x:=0; x < 3; x++ {
				fmt.Println(id, x)
			}
			<- sem  // 接收数据,使得其他阻塞 goroutine 可以发送数据。
		}(i)
	}
}





































