package main

import (
	"fmt"
)

type Human struct {
	name string
	age int
	phone string
}

type Student struct {
	Human //匿名字段Human
	school string
	loan float32
}

type Employee struct {
	Human
	company string
	money float32
}

// 带有接收者的函数称为 method,
// Human对象实现Sayhi方法
func (h *Human) SayHi() {
	fmt.Printf("你好, 我是 %s, 我的电话是 %s \n", h.name, h.phone)
}

func (h *Human) Sing(lyrics string) {
	fmt.Println("lalalalalalala...", lyrics)
}

func (h *Human) Guzzle(beerStein string) {
	fmt.Println("Guzzle, Guzzle, Guzzle...", beerStein)
}

// Employee 重载 Human 的 SayHi 方法
func (e *Employee) SayHi() {
	fmt.Printf("我是 %s, 我在 %s 工作, 我的电话是 %s", e.name, e.company, e.phone)
}

// Student 实现 BorrowMoney 方法
func (s *Student) BorrowMoney(aomout float32) {
	s.loan += aomout
}

// employee 实现 SpendSalary 方法
func (e *Employee) SpendSalary(amount float32) {
	e.money -= amount
}

// 定义 interface
type Men interface {
	SayHi()
	Sing(lyrics string)
	// BorrowMoney(amount float32)
}

type YoungChap interface {
	 SayHi()
	 Sing(song string)
	 BorrowMoney(amount float32)
}

type ElderlyGent interface {
	SayHi()
	Sing(song string)
	SpendSalary(amount float32)
}

func main() {
	mike := &Student{Human{"Mike", 25, "222-222-XXX"}, "MIT", 0.00}
	paul := &Student{Human{"Paul", 26, "111-222-XXX"}, "Harvard", 100}
	sam := &Employee{Human{"Sam", 36, "444-222-XXX"}, "Golang Inc.", 1000}
	tom := &Employee{Human{"Tom", 37, "222-444-XXX"}, "Things Ltd.", 5000}

	//定义Men类型的变量i
	var i Men

	//i能存储Student
	i = mike
	fmt.fmt.Println("This is Mike, a Student:")
	i.SayHi()
	i.Sing("November rain")

	//i也能存储Employee
	i = tom
	fmt.fmt.Println("This is tom, an Employee:")
	i.SayHi()
	i.Sing("Born to be wild")

	//定义了slice Men
	fmt.fmt.Println("Let's use a slice of Men and see what happens")
	x := make([]Men, 3)
	//这三个都是不同类型的元素，但是他们实现了interface同一个接口
	x[0], x[1], x[2] = paul, sam, mike

	for _, value := range x{
		value.SayHi()
	}

}




