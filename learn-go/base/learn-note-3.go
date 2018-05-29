package main

import (
	"fmt"
	"os"
	"errors"
)

// 函数
// 不支持 嵌套 (nested)、重载 (overload) 和 默认参数 (default parameter)。
// 无需声明原型。
// 支持不定长变参。
// 支持多返回值。
// 支持命名返回参数。
// 支持匿名函数和闭包。
func main() {
	s1 := test1(func() int {  // 直接将匿名函数当参数
		return 100
	})

	s2 := format(func(s string, x, y int) string {
		return fmt.Sprintf(s, x, y)
	}, "%d, %d", 10, 20)

	fmt.Println(s1, s2)

	// 变参
	var n2 = []int{1, 2, 3}
	fmt.Println(test2("sum: %d", n2...))

	// 不能用容器对象接收多返回值。只能用多个变量,或 "_" 忽略。
	x, _ := test3()
	fmt.Println(x)


	// 多返回值可直接作为其他函数调用用实参。
	fmt.Println(add2(test4()))
	fmt.Println(sum2(test4()))

	// 命名返回参数可看做与形参类似的局部变量,最后由 return 隐式返回。
	fmt.Println(add3(1, 2))

	// 命名返回参数可被同名局部变量遮蔽,此时需要显式返回。
	fmt.Println(add4(1, 2))

	// 命名返回参数允许 defer 延迟调用通过闭包读取和修改。
	fmt.Println(add5(1, 2))

	// 匿名函数
	// 匿名函数可赋值给变量,做为结构字段,或者在 channel 里传送。
	test5()


	// 延迟调用
	test6()
	// 多个 defer 注册,按 FILO 次序执行。哪怕函数或某个延迟调用发生错误,这些调用依旧会被执行。
	test7(0)

	// 延迟调用参数在注册时求值或复制,可用指针或闭包 "延迟" 读取。
	test8()


	// 错误处理
	test9()
	// 延迟调用中引发的错误,可被后续延迟调用捕获,但仅最后一个错误可被捕获。
	test10()
	test11()
	switch z, err := div(10 , 0); err {
	case nil:
		fmt.Println(z)
	case ErrDivByZero:
		panic(err)
	}
}

// 类型相同的相邻参数可合并。 多返回值必须用括号。
func test(x, y int, s string) (int, string) {
	n := x + y
	return n, fmt.Sprintf(s, n)
}


// 函数是第一类对象,可作为参数传递。建议将复杂签名定义为函数类型,以便于阅读
func test1(fn func() int) int {
	return fn()
}

type FormatFunc func(s string, x, y int) string		// 定义函数类型

func format(fn FormatFunc, s string, x, y int) string {
	return fn(s, x, y)
}

// 变参
// 变参本质上就是 slice。只能有一个,且必须是最后一个。
func test2(s string, n ... int) string {
	var x int
	for _, i := range n {
		x += i
	}
	return fmt.Sprintf(s, x)
}


// 返回值
func test3() (int, int) {
	return 1, 2
}

// 多返回值可直接作为其他函数调用用实参。
func test4() (int, int) {
	return 1, 2
}

func add2(x, y int) int {
	return x + y
}

func sum2(n ...int) int {
	var x int
	for _, i :=range n {
		x += i
	}

	return x
}


// 命名返回参数
// 命名返回参数可看做与形参类似的局部变量,最后由 return 隐式返回。
func add3(x, y int) (z int) {
	z = x + y
	return
}

// 命名返回参数可被同名局部变量遮蔽,此时需要显式返回。
func add4(x, y int) (z int) {
	{	// 不能在同一级别, 引发 "z redeclared in this block" 错误。
		var z = x + y
		// return  // Error: z is shadowed during return
		return z   // 必须显式返回。
	}
}

// 命名返回参数允许 defer 延迟调用通过闭包读取和修改。
func add5(x, y int) (z int) {
	defer func() {
		z += 100
	}()

	z = x + y
	return
}


// 匿名函数
// 匿名函数可赋值给变量,做为结构字段,或者在 channel 里传送。
func test5() {
	// 函数变量
	fn := func() { println("hello world")}
	fn()

	// 函数集合
	fns := []func(x int) int {
		func(x int) int { return x + 1 },
		func(x int) int { return x + 2 },
	}
	fmt.Println(fns[1](100))
	
	// 函数 field
	d := struct {
		fn func() string
	}{
		fn: func() string {
			return "hello world"
		},
	}
	fmt.Println(d.fn())

	// channel
	fc := make(chan func() string, 2)
	fc <- func() string { return "hello world"}
	fmt.Println("channel", (<-fc)())
}


// 延迟调用
// 关键字 defer 用于注册延迟调用。这些调用直到 return 前才被执行行,通常用于释放资源或错误处理。
func test6() error {
	f, err := os.Create("test.txt")
	if err != nil { return err }
	defer f.Close()		// 注册调用, 而不是注册函数.必须提供参数,哪怕为空。
	f.WriteString("hello world")
	return nil
}

// 多个 defer 注册,按 FILO 次序执行。哪怕函数或某个延迟调用发生错误,这些调用依旧会被执行。
func test7(x int) {
	defer println("a")
	defer println("b")

	//defer func() {
	//	println(100/x)
	//}()

	defer println("c")

	//输出
	//c
	//b
	//a
	//panic: runtime error: integer divide by zero
}

// 延迟调用参数在注册时求值或复制,可用指针或闭包 "延迟" 读取。
func test8() {
	x, y := 10, 20

	defer func(i int) {
		println("defer", i, y)  // y 闭包引用
	}(x)  // x 被复制

	x += 100
	y += 100
	println("x=", x, "y=", y)

	//x= 110 y= 120
	//defer 10 120
}
// 滥用 defer 可能会导致性能问题,尤其是在一一个 "大循环" 里。


// 错误处理
// 没有结构化异常,使用 panic 抛出错误,recover 捕获错误。
func test9() {
	defer func() {
		if err := recover(); err != nil {
			println(err.(string))
		}
	}()

	panic("panic error")
}

// 延迟调用中引发的错误,可被后续延迟调用捕获,但仅最后一个错误可被捕获。
func test10() {
	defer func() {
		fmt.Println(recover())  // defer panic
	}()

	defer func() {
		panic("defer panic")
	}()

	panic("test panic")
}

// 捕获函数 recover 只有在延迟调用内直接调用才会终止错误,否则总是返回 nil。任何未捕获的错误都会沿调用堆栈向外传递。
func test11() {
	defer recover()  // 无效
	defer fmt.Println(recover())  // 无效

	defer func() {
		func() {
			println("defer inner")
			recover() // 无无效!
		}()
	}()

	// panic("test panic")
}

// 如果需要保护代码片段,可将代码块重构成匿名函数,如此可确保后续代码被执行。
// 除用 panic 引发中断性错误外,还可返回 error 类型错误对象来表示函数调用状态。
// 标准库 errors.New 和 fmt.Errorf 函数用于创建实现 error 接口的错误对象。通过判断错误对象实例来确定具体错误类型。
// 导致关键流程出现不可修复性错误的使用 panic,其他使用 error。
var ErrDivByZero = errors.New("division by zero")

func div(x, y int) (int, error) {
	if y==0 {return 0, ErrDivByZero}
	return x / y, nil
}



