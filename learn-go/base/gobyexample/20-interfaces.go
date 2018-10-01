package main

import (
	"fmt"
	"math"
)

// 接口是方法签名的集合

// 几何图形的一个接口
type geometry interface {
	area() float64
	perim() float64
}

// 矩形
type rect2 struct {
	width, height float64
}

// 圆形
type circle struct {
	radius float64
}

// 矩形面积
func (r rect2) area() float64 {
	return r.width * r.height
}

// 矩形周长
func (r rect2) perim() float64 {
	return 2 * (r.width + r.height)
}


// 圆形面积
func (c *circle) area() float64 {
	return math.Pi * math.Pow(c.radius, 2)
}

// 圆形周长
func (c *circle) perim() float64 {
	return 2 * math.Pi * c.radius
}

func measure(g geometry) {
	fmt.Println(g)
	fmt.Println(g.area())
	fmt.Println(g.perim())
}

func main() {
	r := rect2{width: 3, height: 4}
	c := circle{radius: 5}

	measure(r)
	measure(&c)
}
