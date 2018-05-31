package main

import "fmt"

// 方法
// 方法总是绑定对象实例,并隐式将实例作为第一实参 (receiver)。
// 只能为当前包内命名类型定义方法。
// 参数 receiver 可任意命名。如方方法中未曾使用,可省略参数名。
// 参数 receiver 类型可以是 T 或 *T。基类型 T 不能是接口或指针。
// 不支持方法重载,receiver 只是参数签名的组成部分。
// 可用实例 value 或 pointer 调用全部方法,编译器自动转换。
// 没有构造和析构方法,通常用简单工厂模式返回对象实例。
func main() {
	// receiver T 或 *T
	test_5_1()
	// 匿名字段
	test_5_2()
}

type Queue struct {
	elements []interface{}
}

// 创建对象实例。
func NewQueue() *Queue {
	return &Queue{make([]interface{}, 10)}
}

// 省略 receiver 参数名。
func (*Queue) Push(e interface{}) error {
	panic("not implemented")
}

//func (Queue) Push(e int) error {
//	panic("not implemented")  //Error: method redeclared: Queue.Push
//}

func (self *Queue) length() int {
	// receiver 参数名可以是 self、this 或其他。
	return len(self.elements)
}

// 方法不过是一种特殊的函数,只需将其还原,就知道 receiver T(值传递) 和 *T(引用传递) 的差别。
type Data struct {
	x int
}

// func ValueTest(self Data)
func (self Data) ValueTest() {
	fmt.Printf("value: %p\n", &self)
}

// func PointerTest(self *Data);
func (self *Data) PointerTest() {
	fmt.Printf("pointer: %p\n", self)
}

func test_5_1() {
	d := Data{}
	p := &d
	fmt.Printf("data pointer: %p\n", p)

	d.ValueTest()    // ValueTest(d)
	d.PointerTest()  // PointerTest(&d)

	p.ValueTest()    // ValueTest(*p)
	p.PointerTest()  // PointerTest(p)

	// data pointer: 0xc420090010
	// value: 0xc420090018
	// pointer: 0xc420090010
	// value: 0xc420090030
	// pointer: 0xc420090010
}

// 匿名字段
// 可以像字段成员那样访问匿名字段方法,编译器负责查找。
// 通过匿名字段,可获得和继承类似的复用能力力。依据编译器查找次序,只需在外层定义同名方方法,就可以实现 "override"。
type User struct {
	id int
	name string
}

type Manager struct {
	User
}

func (self *User) ToString() string {
	return fmt.Sprintf("User: %p, %v", self, self)
}


func test_5_2() {
	m := Manager{User{1, "Tom"}}

	fmt.Printf("Manager: %p \n", &m)
	fmt.Println(m.ToString())
}

// 方法集
// 每个类型都有与之关联的方法集,这会影响到接口实现规则。
// 类型 T 方法集包含全部 receiver T 方法。
// 类型 *T 方法集包含全部 receiver T + *T 方方法。
// 如类型 S 包含匿名字段 T,则 S 方方法集包含 T 方方法。
// 如类型 S 包含匿名字段 *T,则 S 方方法集包含 T + *T 方法。
// 不管嵌入 T 或 *T,*S 方法集总是包含 T + *T 方方法。

// 根据调用者不同,方法分为两种表现形式
// instance.method(args...)  --->   <type>.func(instance, args...)
// 前者称为 method value,后者 method expression。
// 两者都可像普通函数那样赋值和传参,区别在于 method value 绑定实例, 而 method expression 则须显式传参。
func (self *User) Test()  {
	fmt.Printf("%p, %v \n", self, self)
}

func test_5_3() {
	u := User{1, "tom"}
	u.Test()

	mValue := u.Test
	mValue()  // 隐式传递 receiver

	mExpression := (*User).Test
	mExpression(&u)  // 显式传递 receiver

}




















