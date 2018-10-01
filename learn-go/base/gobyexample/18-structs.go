package main

import "fmt"

type person struct {
	name string
	age int
}

func main() {
	fmt.Println(person{"Bob", 20})

	fmt.Println(person{name: "alice", age: 30})

	fmt.Println(person{name: "Fred"})

	fmt.Println(&person{name: "Ann", age:50})

	s := person{name: "Sean", age:50}
	fmt.Println(s.name)

	// 指针会自动解除引用
	sp := &s
	fmt.Println(sp.age)

	// 结构体是可变的
	sp.age = 51
	fmt.Println(sp.age)
}
