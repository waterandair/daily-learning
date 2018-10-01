package main

import "fmt"

type rect struct {
	width, height int
}

// 传入指针
func (r *rect) area() int {
	return r.width * r.height
}

// 传入值
func (r rect) perim() int {
	return 2 * (r.width + r.height)
}

// 对比传入指针类型和值类型在修改时的不同
func (r *rect) update(width, height int) {
	r.width = width
	r.height = height
}

func (r rect) update2(width, height int) {
	r.width = width
	r.height = height
}

func main() {
	r := rect{width: 10, height: 5}

	// 面积
	fmt.Println("area: ", r.area())  // 50
	// 周长
	fmt.Println("perim:", r.perim())  // 30

	rp := &r
	fmt.Println(rp.area())  // 50
	fmt.Println(rp.perim())  // 30

	// go 会自动处理方法调用的值和指针之间的转换
	// 你可能需要传入指针类型以避免复制， 或者允许方法对传入的结构体进行修改

	fmt.Println("r:", r)  // r: {10 5}
	r.update(1,1)
	fmt.Println("r update:", r)  // r update: {1 1}
	r.update2(2, 2)
	fmt.Println("r update2", r)  // r update2 {1 1}
}
