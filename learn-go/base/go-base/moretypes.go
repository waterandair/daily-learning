package main

import "fmt"

func main() {
	//pointer()
	//structDemo()
	//array()
	//slice()
	//makeSlice()
	//nilSlice()
	forRange()
	// mapDemo()
	//updateMap()
	//
	//// 闭包
	//c := adder()
	//fmt.fmt.Println(c(1))
	//fmt.fmt.Println(c(5))
	//
	//fmt.fmt.Println("斐波那契数列")
	//// 斐波那契
	//f := fibonacci()
	//for i := 0; i < 10; i++ {
	//	fmt.fmt.Println(f())
	//}
	//
	//// 斐波那契
	//fmt.fmt.Println(fibonacci2(6))
}

func pointer() {
	i, j := 42, 2701

	// & 符号会生成一个指向其作用对象的指针。
	p := &i
	// * 符号表示指针指向的底层的值。
	fmt.fmt.Println(*p)  // 通过指针读取 i 的值
	*p = 21  // 通过指针设置 i 的值
	fmt.fmt.Println("i: ", i)

	p = &j
	*p = *p / 37
	fmt.fmt.Println("j: ", j)
}

func structDemo() {
	type Vertex struct {
		X int
		Y int
	}
	v := Vertex{1, 2}
	fmt.fmt.Println(v)
	fmt.fmt.Println(v.X)  // 结构体字段使用点号来访问
	p := &v
	p.X = 3  // 结构体字段可以通过结构体指针访问,通过指针间接的访问是透明的
	fmt.fmt.Println(v)
}

// 类型 [n]T 是一个有 n 个类型为 T 的值的数组。
func array() {
	var a [2]string
	a[0] = "Hello"
	a[1] = "World"
	fmt.fmt.Println(a[0], a[1])
	fmt.fmt.Println(a)
}

// 一个 slice 会指向一个序列的值，并且包含了长度信息。 []T 是一个元素类型为 T 的 slice。
func slice() {
	p := []int{2, 3, 4}
	fmt.fmt.Println("p ==", p)

	for i := 0; i < len(p); i++ {
		fmt.Printf("p[%d] == %d \n", i, p[i])
	}

	fmt.fmt.Println("p[1:2]", p[1:2])
	fmt.fmt.Println("p[:3]", p[:3])
}

// make 函数可以创建一个 slice
func makeSlice() {
	a := make([]int, 5)
	fmt.Printf("%s len=%d cap=%d %v\n", "a", len(a), cap(a), a)

	b := make([]int, 0, 5)
	fmt.Printf("%s len=%d cap=%d %v\n", "b", len(b), cap(b), b)

	c := b[:2]
	fmt.Printf("%s len=%d cap=%d %v\n", "c", len(c), cap(c), c)

	d := c[2:5]
	fmt.Printf("%s len=%d cap=%d %v\n", "d", len(d), cap(d), d)
}

func nilSlice() {
	var z []int
	fmt.fmt.Println(z, len(z), cap(z))

	if z == nil {
		fmt.fmt.Println("nil")
	}

	z = append(z, 1)
	fmt.fmt.Println(z, len(z), cap(z))
}

// for 循环的 range 格式可以对 slice 或者 map 进行迭代循环。
func forRange() {
	pow := []int{1, 2, 3}
	arr := [3]int{1, 3, 4}
	for i, v := range pow {
		fmt.fmt.Println(i, v)
	}

	// 如果要去掉索引值,用下划线替代
	for _, v := range pow {
		fmt.fmt.Println(v)
	}

	for _, v := range arr {
		fmt.Println(v)
	}
}

type Vertex struct {
	Lat, Long float64
}
// map 在使用之前必须用 make 而不是 new 来创建；值为 nil 的 map 是空的，并且不能赋值。
func mapDemo() {
	var m map[string]Vertex
	// 先定义再使用必须使用 make 函数
	m = make(map[string]Vertex)
	m["Bell Labs"] = Vertex{
		40.68433, -74.39967,
	}
	fmt.fmt.Println(m["Bell Labs"])

	var n = map[string]Vertex{
		"Bell Labs": Vertex{
			40.68433, -74.39967,
		},
		"Google": Vertex{
			37.42202, -122.08408,
		},
	}
	fmt.fmt.Println(n)

	// 如果顶级的类型只有类型名的话，可以在文法的元素中省略键名。
	var l = map[string]Vertex{
		"Bell Labs": {40.68433, -74.39967},
		"Google":    {37.42202, -122.08408},
	}
	fmt.fmt.Println(l)
}

func updateMap() {
	m := make(map[string]int)

	m["answer"] = 42
	fmt.fmt.Println(m)

	m["answer"] = 48
	fmt.fmt.Println(m)

	delete(m, "answer")
	fmt.fmt.Println(m["answer"])  // 0

	// 返回的第二个值表示 是否取到值
	v, ok := m["answer"]
	fmt.fmt.Println(v, ok)
}

// 闭包是一个函数值，它来自函数体的外部的变量引用。 函数可以对这个引用值进行访问和赋值；换句话说这个函数被“绑定”在这个变量上。
func adder() func(int) int {
	sum := 0
	return func(x int) int {
		sum += x
		return sum
	}
}

func fibonacci() func() int {
	f1, f2, f0:= 1, 1, 0
	index := -1
	return func () int {
		index ++
		if index == 0 {
			return 1
		} else if index == 1 {
			return 1
		} else {
			f0 = f1 + f2
			f1 = f2
			f2 = f0
			return f0
		}
	}
}

func fibonacci2(n int) int{
	if n <= 2 {
		return 1
	} else {
		return fibonacci2(n-1) + fibonacci2(n-2)
	}

}




