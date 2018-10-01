package main

import (
	"errors"
	"fmt"
)

func f1(arg int) (int, error) {
	if arg == 42 {
		// 按照管理，最后一个返回值为错误类型
		return -1, errors.New("can't work with 42")
	}

	// 用 nil 表示没有错误
	return arg + 3, nil
}


// 自定义错误类型，只要实现 Error() 方法即可
type argError struct {
	arg int
	prob string
}

func (e *argError) Error() string {
	return fmt.Sprintf("%d - %s", e.arg, e.prob)
}

func f2(arg int) (int, error) {
	if arg == 42 {
		return -1, &argError{arg, "can't work with it"}
	}
	return arg + 3, nil
}


func main() {
	for _, i := range []int{7, 42} {
		if r, e := f1(i); e!= nil{
			fmt.Println("f1 failed:", e)
		} else {
			fmt.Println("f1 worked:", r)
		}
	}

	for _, i := range []int{7, 42} {
		if r, e := f2(i); e!= nil{
			fmt.Println("f2 failed:", e)
		} else {
			fmt.Println("f2 worked:", r)
		}
	}


	// 如果要在自定义错误中以编程的方式使用数据，需要通过类型断言将错误作为自定义错误类型的实例
	_, e := f2(42)
	if ae, ok := e.(*argError); ok {
		fmt.Println(ae.arg)
		fmt.Println(ae.prob)
	}
}
