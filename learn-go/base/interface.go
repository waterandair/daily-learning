package main

import (
	"log"
	"fmt"
)

/*
接口（非侵入式）
	接口是一个或多个方法签名的集合,任何类型的方法集中只要拥有与之对应的全部方法,就表示它 "实现" 了该接口,无须在该类型上显式添加接口声明。
	所谓对应方法,是指有相同名称、参数列表 (不包括参数名) 以及返回值。当然,该类型还可以有其他方方法。
	接口命名习惯以 I 开头， er 结尾
	接口只有方法签名,没有实现。接口没有数据字段。
	可在接口中嵌入其他接口。
	类型可实现多个接口。
	空接口 interface{} 没有任何方法签名,也就意味着任何类型都实现了空接口。其作用类似面向对象语言中的根对象 object。

	执行机制
	接口对象由接口表 (interface table) 指针和数据指针组成。
	接口表存储元数据信息,包括接口类型、动态类型,以及实现接口的方法指针。无论是反射还是通过接口调用方方法,都会用到这些信息。

	Go语言中任何对象实例都满足空接口 interface{} ,所以 interface{} 看起来像是可以指向任何对象的 Any 类型
*/


func main() {
	test_6_2()

}

/*
接口赋值
	- 将对象实例赋值给接口
	- 将一个接口赋值给另一个接口
要求该对象实例实现了接口要求的所有方法


*/

type Integer int

func (a Integer) Less(b Integer) bool {
	return a < b
}

func (a *Integer) Add(b Integer) {
	*a += b
}

type ILessAdder interface {
	Less(b Integer) bool
	Add(b Integer)
}

type Lesser interface {
	Less(b Integer) bool
}

func interfaceAssignment()  {
	var a Integer = 1
	var b ILessAdder = &a
	/*
		自动生成方法：
		func (a *Integer) Less(b Integer) bool {
			return (*a).Less(b)
		}
		这样,类型 *Integer 就既存在 Less() 方法,也存在 Add() 方法,满足 LessAdder 接口

		如果使用这样的方式：
		var b ILessAdder = a
		无法自动生成方法：
		func (a Integer) Add(b Integer) {
			(&a).Add(b)
		}
		因此,类型 Integer 只存在 Less() 方法
	*/

	// 对于 Lesser 接口，这两种方式都是可以编译通过的
	var c1 Lesser = &a
	var c2 Lesser = a


	log.Println(b, c1, c2)
}

/*
接口查询
	var file1 Writer = ...
	if file5, ok := file1.(two.IStream); ok {
		...
	}
*/


/*
类型查询：
	在Go语言中,还可以更加直截了当地询问接口指向的对象实例的类型

	var v1 interface{} = ...
		switch v := v1.(type) {
		case int:
		// 现在v的类型是int
		case string: // 现在v的类型是string
		...
}

Go语言标准库的 Println() 比这个例子要复杂很多,我们这里只摘取其中的关键部
分进行分析。对于内置类型, Println() 采用穷举法,将每个类型转换为字符串进行打印。对
于更一般的情况,首先确定该类型是否实现了 String() 方法,如果实现了,则用 String() 方
法将其转换为字符串进行打印。否则, Println() 利用反射功能来遍历对象的所有成员变量进
行打印。
*/

/*
接口组合：
	类似类型组合。可以认为接口组合是类型匿名组合的一个特定场景,只不过接口只包含方法,而不包含任何
成员变量
	比如 Go语言包中有 io.Reader接口和 io.Writer 接口，还有一个 io.ReadWriter 接口
	// ReadWriter接口将基本的Read和Write方法组合起来
	type ReadWriter interface {
		Reader
		Writer
	}

	等价于：
	type ReadWriter interface {
		Read(p []byte) (n int, err error)
		Write(p []byte) (n int, err error)
	}

*/

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

	fmt.Printf("%v \n", u)  // {2 jack}
	fmt.Printf("%v \n", i.(User))  // {1 tom}

	// 接口转型返回临时对象,只有使用指针才能修改其状态。
	u2 := User{1, "Tom"}
	var vi, pi interface{} = u2, &u2
	// vi.(User).name = "jack1"  // cannot assign to vi.(User).name
	pi.(*User).name = "jack2"

	fmt.Printf("%v \n", vi.(User))  // {1 Tom}
	fmt.Printf("%v \n", pi.(*User))  // &{1 jack2}
}





