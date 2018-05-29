package main

import (
	"fmt"
	"unsafe"
)
type any interface{}

func print(name string, vals ... any) {
	fmt.Println("************** " + name + " **************")
	fmt.Println(vals)
	fmt.Println("----------------------------------------")
}

func main() {
	// 变量
	test_1_1()
	// 常量
	test_1_2()
	// 引用类型
	test_1_4()
	// 类型转换
	test_1_5()
	// 字符串
	test_1_6()
	// 指针
	test_1_7()

}

func test_1_1() {
	// 多变量赋值时,先计算所有相关值,然后再从左到右依次赋值。
	data, i := [3]int{0, 1, 2}, 0
	i, data[i] = 2, 100
	print("test_1_1", i, data)
}

func test_1_2() {
	// 常量不能使用 := 定义
	const a int = 1  // 未使用局部常量不会引发编译错误

	// 不提供类型和初始化值,那么视作与上一一常量相同
	const (
		s = "abc"
		x  // x= "abc"
		b = len(s)
		c = unsafe.Sizeof(b)
	)

	// 枚举
	const (
		Sunday = iota // 0
		Monday // 1,通常省略后续行行表达式。
		Tuesday // 2
		Wednesday // 3
		Thursday // 4
		Friday // 5
		Saturday // 6
	)

	const (
		_ = iota 						// iota = 0
		KB int64 = 1 << (10 * iota) 	// iota = 1
		MB 								// 与 KB 表达式相同,但 iota = 2
		GB
		TB
	)

	// 在同一常量组中,可以提供多个 iota,它们各自自增⻓长
	const (
		A, B = iota, iota << 10 // 0, 0 << 10
		C, D // 1, 1 << 10
	)

	print("test_1_2", x, b, c, Saturday, TB, C, D)
}

func test_1_4() {
	// 内置函数 new 计算类型大小,为其分配零值内存,返回指针。而 make 会被编译器翻译
	// 成具体的创建函数,由其分配内存和初始化成员结构,返回对象而非指针。
	a := []int{0, 0, 0}
	// 提供初始化表达式。
	fmt.Println(a)
	a[1] = 10
	fmt.Println(a)
	b := make([]int, 3)
	fmt.Println(b)
	// makeslice
	b[1] = 10
	fmt.Println(b)
	//c := new([]int)  // c[1] = 10 // Error: invalid operation: c[1] (index of type *[]int)
}

func test_1_5() {
	// 不支支持隐式类型转换,即便是从窄向宽转换也不行。
	var b byte = 100
	// var n int = b // Error: cannot use b (type byte) as type int in assignment
	var n int = int(b) // 显式转换

	// 不能将其他类型当 bool 值使用用。
	//a := 100
	// if a {}   // Error: non-bool a (type int) used as if condition

	print("test_1_5", n)
}

func test_1_6() {
	// 字符串是不可变值类型,内部用用指针指向 UTF-8 字节数组。
	// 默认值是空字符串 ""。
	// 用索引号访问某字节,如 s[i]。
	// 不能用序号获取字节元素指针,&s[i] 非法。
	// 不可变类型,无法修改字节数组。
	// 字节数组尾部不包含 NULL。
	s := "abc"

	// 使用 ` 定义不做转义处理的原始字符串,支持跨行
	ss := `a
          b\r\n\x00
          c`
	sss := "Hello world"  // 支持索引

	a := 'a'  // 单引号字符常量表示示 Unicode Code Point,支支持 \uFFFF、\U7FFFFFFF、\xFF 格式
	var c1, c2 rune = '\u6211', '们'

	// 修改字符串需要把字符串转为 []rune 或 []byte, 完成后再转为 string
	// byte 是 int8  适合表示 ascii 编码
	// rune 是 int32  适合表示 unicode 编码
	s1 := "abcd"
	bs := []byte(s1)
	bs[1] = 'B'
	s1 = string(bs)

	u := "电脑"
	us := []rune(u)
	us[1] = '话'
	u = string(us)

	// for 循环遍历字符串也有两种方法
	s2 := "abc汉字"
	s2_slice := make([]string, 0)
	for i := 0; i < len(s2); i++ {
		// byte, 不能表示汉字
		s2_slice = append(s2_slice, string(s2[i]))
	}


	print("test_1_6", s[0] == '\x61', s[1] == 'b', s[2] == 0x63,
		ss, sss[:5], a, c1 == '我', string(c2) == "\xe4\xbb\xac",
		s1, u, s2, s2_slice)
}

func test_1_7() {
	// 支持指针类型 *T,指针的指针 **T,以及包含包名前缀的 *<package>.T。
	// 操作符 "&" 取变量地址,"*" 透过指针访问目标对象。
	// 不支持指针运算,不支支持 "->" 运算符,直接用用 "." 访问目标成员。
	type data struct {a int}
	var d = data{1234}
	var p *data
	p = &d

	// 可以在 unsafe.Pointer 和任意类型指针间进行转换。
	x := 0x12345678
	p2 := unsafe.Pointer(&x)  // int指针转为通用指针Pointer
	n := (*[4]byte)(p2)  // Pointer 指针转为 *[4]byte 指针
	for _,i:= range n {
		fmt.Printf("%X", i)
	}
	print("test_1_7", p, p.a)

}