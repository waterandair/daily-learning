package main

import (
	"fmt"
	"math/rand"
	"math"
	"math/cmplx"
)

// 变量的定义“打包”在一个语法块中。
var (
	ToBe bool = false
	MaxInt uint64 = 1 << 64 - 1
	z complex128 = cmplx.Sqrt(-5 + 12i)
	/* go 数据类型
	bool
	string
	int  int8  int16  int32  int64
	uint uint8 uint16 uint32 uint64 uintptr
	byte // uint8 的别名
	rune // int32 的别名 代表一个Unicode码
	float32 float64
	complex64 complex128
	*/
)



func main() {
	fmt.Printf("hello, world\n")
	fmt.Println("My favorite number is ", rand.Intn(20))
	fmt.Printf("Now you have %g problems.\n", math.Nextafter(1, 3))
	// 被导出的名称首字母必须大写
	fmt.Println(math.Pi)
	fmt.Println(add(1, 2))
	// := 简洁赋值语句在明确类型的地方,可以替代 var 定义,在函数外不能使用
	a, b := swap("hello", "world")
	fmt.Println(a, b)
	fmt.Println(split(11))
	var i int
	fmt.Println(i, c, python, java)

	// 常量不能使用 := 定义
	const f = "%T(%v)\n"
	fmt.Printf(f, ToBe, ToBe)
	fmt.Printf(f, MaxInt, MaxInt)
	fmt.Printf(f, z, z)

	// 类型转换, 需要显示
	var x, y = 3, 4
	var f2 = math.Sqrt(float64(x*x + y*y))
	var z = int(f2)
	fmt.Println(x, y, z)
}

// 变量在定义是没有赋值,会初始化为 零值 0, false, ""
var c, python, java bool

// 多个连续的命名参数是同一类型,可以只写最后一个参数的变量声明
func add(x int, y int) int {
	return x + y
}

// 函数可以返回多个返回值
func swap(x, y string) (string, string){
	return y, x
}

// 没有参数的 return 语句返回结果的当前值。也就是`直接`返回。
// 直接返回语句仅应当用在像下面这样的短函数中。在长的函数中它们会影响代码的可读性
func split(sum int)(x, y int) {
	x = sum * 4 / 9
	y = sum -x
	return
}



