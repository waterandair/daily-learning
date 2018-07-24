package main

import "log"

func main() {

}

// 只要实现了 Error 方法，就可以自定义错误类型
type PathError struct {
	Op string
	Path string
	Err error
}

func (e *PathError) Error() string{
	return e.Op + " " + e.Path + ": " + e.Err.Error()
}

/*
panic 错误处理流程

- 调用 panic()
- 程序执行立即停止
- 之前定义的 defer 将正常执行
- 之后该函数返回到调用函数并导致逐级向上执行 panic 流程
- 直到所属的 goroutine 中所有正在执行的函数被终止
*/

/*
recover() 函数用于终止错误处理流程

recover() 应该在一个使用defer关键字的函数中执行，用于截取错误处理流程
如果没有在发生异常的 goroutine 中调用恢复过程，会导致该 goroutine 所属的进程直接退出
*/
func foo() {
	defer func() {
		// 如果 foo 函数中出发了错误处理流程，recover 会是错误处理过程终止，且会获取到详细的信息
		if r := recover(); r != nil {
			log.Printf("Runtime error caught: %v", r)
		}
	}()
}


