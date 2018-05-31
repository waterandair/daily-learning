package main
// 包
import (
	// "fmt"
	// "yuhen/test" // 默认模式: test.A
	// M "yuhen/test" // 包重命名: M.A
	// . "yuhen/test" // 简便模式: A
	// _ "yuhen/test" // 非导入模式: 仅让该包执行初始化函数。
	"fmt"
	"time"
)

// 初始化函数
// 每个源文文件都可以定义一个或多个初始化函数。
// 编译器不保证多个初始化函数执行次序。
// 初始化函数在单一线程被调用,仅执行一次。
// 初始化函数在包所有全局变量初始化后执行。
// 在所有初始化函数结束后才执行 main.main。
// 无法调用初始化函数。

var now = time.Now()
//func init() {
//	fmt.Printf("now: %v\n", now)
//}
//func init() {
//	fmt.Printf("since: %v\n", time.Now().Sub(now))
//}

// 可在初始化函数中使用 goroutine,可等待其结束。
func main() {
	fmt.Println("main:", int(time.Now().Sub(now).Seconds()))
}

func init() {
	fmt.Println("init:", int(time.Now().Sub(now).Seconds()))
	w := make(chan bool)
	go func() {
		time.Sleep(time.Second * 3)
		w <- true
	}()
	<-w
}

// 不应该滥用初始化函数,仅适合完成当前文件中的相关环境设置。