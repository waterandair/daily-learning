package main

import "fmt"

// 接口
// 接口是一个或多个方法签名的集合,任何类型的方法集中只要拥有与之对应的全部方法,
// 就表示它 "实现" 了该接口,无须在该类型上显式添加接口声明。
// 所谓对应方法,是指有相同名称、参数列表 (不包括参数名) 以及返回值。当然,该类型还
// 可以有其他方方法。
// 接口命名习惯以 er 结尾,结构体。
// 接口只有方法签名,没有实现。
// 接口没有数据字段。
// 可在接口中嵌入其他接口。
// 类型可实现多个接口。
// 空接口 interface{} 没有任何方法签名,也就意味着任何类型都实现了空接口。其作用类似面向对象语言中的根对象 object。

// 执行机制
// 接口对象由接口表 (interface table) 指针和数据指针组成。
// 接口表存储元数据信息,包括接口类型、动态类型,以及实现接口的方法指针。无论是反射还是通过接口调用方方法,都会用到这些信息。


func main() {
	test_6_2()
}


// 数据指针持有的是目标对象的只读复制品,复制完整对象或指针。
func test_6_2() {
	type User struct {
		id int
		name string
	}

	u := User{1, "tom"}
	var i interface{} = u

	u.id = 2
	u.name = "jack"

	fmt.Printf("%v \n", u)
	fmt.Printf("%v \n", i.(User))

	// 接口转型返回临时对象,只有使用指针才能修改其状态。
	u2 := User{1, "Tom"}
	var vi, pi interface{} = u2, &u2
	// vi.(User).name = "jack1"  // cannot assign to vi.(User).name
	pi.(*User).name = "jack2"

	fmt.Printf("%v \n", vi.(User))
	fmt.Printf("%v \n", pi.(*User))
	//
	//{2 jack}
	//{1 tom}
	//{1 Tom}
	//&{1 jack2}

}




