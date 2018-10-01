package main

import "os"

// panic 同于快速以并不优雅的方式处理异常。
// 当函数返回一个我们不知道如何处理的 error 是， 可以使用 panic
// 不同于大多数语言使用 exception 处理许多 error， go 语言惯用的是尽可能返回错误码
func main() {
	panic("a problem")

	_, err := os.Create("/tmp/file")
	if err != nil {
		panic(err)
	}
}

