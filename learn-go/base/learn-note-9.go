package main

import (
	"reflect"
	"fmt"
)

// 反射
// 没有运行期类型对象,实例也没有附加字段用来表明身身份。只有转换成接口时,才会在其
// itab 内部存储与该类型有关的信息,Reflect 所有操作都依赖于此。
func main() {
	test_9_1()
}

// 以 struct 为例,可获取其全部成员字段信息,包括非导出和匿名字段。
func test_9_1() {

	type User struct {
		UserName string
	}

	type Admin struct {
		User
		title string
	}

	var u Admin
	t := reflect.TypeOf(u)

	for i, n := 0, t.NumField(); i < n; i++ {
		f := t.Field(i)
		fmt.Println(f.Name, f.Type)
	}

	// 输出
	// User main.User  可进一步递归
	// title string

	// 如果是指针,应该先使用 Elem 方法获取目标类型,指针本身是没有字段成员的。
	u1 := new(Admin)
	t = reflect.TypeOf(u1)
	if t.Kind() == reflect.Ptr {
		t = t.Elem()
	}

	for i, n := 0, t.NumField(); i < n; i++ {
		f := t.Field(i)
		fmt.Println(f.Name, f.Type)
	}

}