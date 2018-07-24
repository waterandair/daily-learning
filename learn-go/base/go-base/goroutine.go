package main

import (
	"math"
	"fmt"
	"log"
)

/*
并发
	Go 在语言层面对并发编程提供支持,称作 goroutine 的机制。
	只需在函数调用语句前添加 go 关键字,就可创建并发执行单元。
	goroutine 是一种非常轻量级的实现,可在单个进程里执行成千上万的并发任务。

	事实上,入口函数 main 就以 goroutine 运行
	调度器不能保证多个 goroutine 执行次序,且进程退出时不会等待它们结束.
	需要注意的是,如果这个函数有返回值,那么这个返回值会被丢弃
	默认情况下,进程启动后仅允许一个系统线程服务于 goroutine。可使用环境变量或标准
	库函数 runtime.GOMAXPROCS 修改,让调度器用多个线程实现多核并行,而不仅是并发。

并发通信： 不要通过共享内存来通信,而应该通过通信来共享内存。
	channel是进程内的通信方式， 跨进程进程通信建议用 socket
	一个channel只能传递一种类型的值,这个类型需要在声明channel时指定，可以将其认为是一种类型安全的管道

	默认为同步模式，异步方式通过判断缓冲区来决定是否阻塞。如果缓冲区已满,发送被阻塞;缓冲区为空, 接收被阻塞。
	通常情况下,异步 channel 可减少排队阻塞,具备更高的效率。但应该考虑使用指针规避大对象拷⻉,将多个元素打包,减小缓冲区大小等。

*/

func main() {

	// 单向
	channel_demo4()
	// test_7_1()
	// test_7_2()
	// test_7_3()

	// channel
	// test_7_4()

	// test_7_5()
	// 单向
	// test_7_6()
}

func goroutine_demo() {
	/*
	控制台没有输出内容
		Go程序从初始化 main package 并执行 main() 函数开始,当 main() 函数返回时,程序退出,且程序并不等待其他goroutine(非主goroutine)结束
		例子中,主函数启动了10个goroutine,然后返回,这时程序就退出了,而被启动的执行 Add(i, i) 的goroutine没有来得及执行,所以程序没有任何输出
	*/

	/*	for i := 0; i < 10; i ++ {
			go add1(i, i)
		}*/

	/* channel 通信演示 */
	chs := make([]chan int, 10)
	for i := 0; i < 10; i++ {
		chs[i] = make(chan int)
		go count(chs[i], i, i)
	}

	// 在 channel 中的数据被读取前是阻塞的
	for _, ch := range chs {
		<-ch
	}

}

func add1(x, y int) {
	z := x + y
	fmt.Println(z)
}

func count(ch chan int, x, y int) {
	z := x + y
	fmt.Println("counting", z)
	ch <- 1
}

func channel_demo() {
	// 声明
	var ch chan int
	ch2 := make(chan int)
	var m map[string] chan bool

	// 写操作,向channel写入数据通常会导致程序阻塞,直到有其他goroutine从这个channel中读取数据
	ch <- 1
	// 读操作,如果channel之前没有写入数据,那么从channel中读取数据也会导致程序阻塞,直到channel 中被写入数据为止
	value := <- ch

	// 声明一个带缓冲的 channel，达到消息队列的效果,在缓冲区被填完之前都不会阻塞。
	c := make(chan int, 1024)
	// 读取一个带缓冲的 channel， 与普通的一样，但是也可以使用 range
	for i := range c {
		fmt.Println(i)
	}


	log.Println(ch2, m, value, c)
}

// 同步
func channel_demo2() {
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

// 异步
func channel_demo3() {
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
	close(data)  // 判断 channel 是否关闭，用 x, ok := <-ch

	<-exit
}

// 单向 可以将 channel 隐式转换为单向队列,只收或只发。
func channel_demo4() {
	c := make(chan int, 3)

	var send chan<- int = c  // 只发
	var recv <-chan int = c  // 只收

	send <- 1  // 只发
	fmt.Println(<- recv)	   // 只收
}

func sum3(id int) {
	var x int64
	for i := 0; i < math.MaxUint32; i++ {
		x += int64(i)
	}

	println(id, x)
}

