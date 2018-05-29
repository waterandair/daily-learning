package main

import "fmt"

func main() {
	test_slice()
}

// 数组
// 数组是值类型,赋值和传参会复制整个数组,而不是指针。
// 数组⻓长度必须是常量,且是类型的组成部分。[2]int 和 [3]int 是不同类型。
// 支持 "=="、"!=" 操作符,因为内存总是被初始化过的。
// 指针数组 [n]*T,数组指针 *[n]T。
func test_array() {
	// 可用复合语句初始化
	a := [3]int{1, 2}  // 未初始化的元素为 0
	b := [...]int{1, 2, 3, 4}  // 通过初始化值确定数组长度
	c := [5]int{2: 100, 4:200}  // 使用索引号初始化元素
	d := [...]struct{
		name string
		age int8
	}{
		{"user1", 10},
		{"user2", 20},
	}

	// 支持多维数组
	e := [2][3]int{{1, 2, 3}, {4, 5, 6}}
	f := [...][2]int{{1, 1}, {2, 2}, {3, 3}}  // 第二维度不能用 "..."

	// 值拷贝行为会造成性能问题,通常会建议使用slice,或数组指针

	fmt.Sprintf("", a, b, c,d,e,f)
}

// Slice
// 需要说明,slice 并不是数组或数组指针。它通过内部指针和相关属性引用数组片段,以实现变长方案。
// 引用类型。但自身是结构体,值拷贝传递。
// 属性 len 表示可用元素数量,读写操作不能超过该限制。
// 属性 cap 表示最大扩张容量,不能超出数组限制。
// 如果 slice == nil,那么 len、cap 结果都等于 0。
func test_slice() {
	data := [...]int{0,1,2,3,4,5,6}
	slice := data[1:4:5]  // [low:high:max]
	fmt.Println(slice)  // [1 2 3]

	// 读写操作实际的目标是底层数组,只需注意索引号的差别。
	s := data[2:4]
	fmt.Println(s)  // [2 3]
	s[0] += 100
	s[1] += 200
	fmt.Println(s)  // [102 203]
	fmt.Println(data)  // [0 1 102 203 4 5 6]

	// 可直接创建 slice 对象,自动分配底层数组。
	s1 := []int{0, 1, 2, 3, 8: 100}  // 通过初始化表达式构造,可使用用索引号。
	fmt.Println(s1, len(s1), cap(s1))

	s2 := make([]int, 6, 8)  // 使用 make 创建,指定 len 和 cap 值。
	fmt.Println(s2)

	s3 := make([]int, 6) // 省略 cap,相当于 cap = len。
	fmt.Println(s3)

	// 使用 make 动态创建 slice,避免了数组必须用常量做长度的麻烦。还可用指针直接访问底层数组,退化成普通数组操作。
	s4 := []int{0, 1, 2, 3}
	p := &s4[2]  // *int, 获取底层数组元素指针
	*p += 100
	fmt.Println(s4)
}

func test_reslice() {
	
}