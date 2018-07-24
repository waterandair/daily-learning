package main

import (
	"sync"
	"runtime"
	"fmt"
)

/*
sync.Mutex  当一个goroutine获得了 Mutex 后,其他goroutine就只能乖乖等到这个goroutine释放该 Mutex
sync.RWMutex 经典的单写多读模型.读锁占用会阻止写,但不阻止读,而写锁会阻止任何其他goroutine (无论读和写)进来,整个锁相当于由该goroutine独占
sync.Once 全局唯一性操作，once 的 Do() 方法可以保证在全局范围内只调用指定的函数一次,而且所有其他goroutine在调用到此语句时,将会先被阻塞,直至全局唯一的once.Do() 调用结束后才继续。
sync.WaitGroup 用于等待一组 goroutine 结束
*/

func main() {

}

func lock() {
	// 锁的常见使用方式

	var l sync.Mutex

	go func() {
		l.Lock()
		// 执行逻辑代码
		defer l.Unlock()
	}()
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

