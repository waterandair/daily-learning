package main
// 数据
import "fmt"

func main() {
	test_slice()
	test_reslice()
	test_append()
	test_copy()
	test_map()
	test_strut()
	// 匿名字段
	test_struct_anonymous()
	// 面向对象
	test_struct_object()
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
	s1 := []int{0, 1, 2, 3, 8: 100}  // 通过初始化表达式构造,可使用索引号。
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
	// 所谓 reslice,是基于已有 slice 创建新 slice 对象,以便在 cap 允许范围内调整属性。
	s := []int{0, 1, 2, 3, 4, 5, 6, 7, 8, 9}
	s1 := s[2:5] // [2 3 4]
	s2 := s1[2:6:7] // [4 5 6 7]
	// s3 := s2[3:6] // Error
	fmt.Println("s1", s1, "len=", len(s1), "cap=", cap(s1))  // [2 3 4] len= 3 cap= 8
	fmt.Println("s2", s2, "len=", len(s2), "cap=", cap(s2))  // [4 5 6 7] len= 4 cap= 5
}

func test_append() {
	// 向 slice 尾部添加数据,返回新的 slice 对象。
	s := make([]int, 0, 5)
	fmt.Printf("%p\n", &s)   // 0xc42000a1a0

	s2 := append(s, 1)
	fmt.Printf("%p\n", &s2)   // 0xc42000a1c0

	data := [...]int{0, 1, 2, 3, 4, 5, 6, 7, 8, 9}
	s = data[:3]
	s2 = append(s, 100, 200)
	// 添加多个值。
	fmt.Println(data)  // [0 1 2 100 200 5 6 7 8 9]
	fmt.Println(s)  // [0 1 2]
	fmt.Println(s2)  // [0 1 2 100 200]

	// 一旦超出原 slice.cap 限制,就会重新分配底层数组,即便原数组并未填满。
	data2 := [...]int{0, 1, 2, 3, 4, 10: 0}
	s3 := data2[:2:3]
	fmt.Println(s3)
	s3 = append(s3, 100, 200) // 一次 append 两个值,超出 s.cap 限制。
	fmt.Println(s3, data2) // 重新分配底层数组,与原数组无无关。
	fmt.Println(&s3[0], &data2[0]) // 比对底层数组起始指针。

	// 从输出结果可以看出,append 后的 s 重新分配了底层数组,并复制数据。如果只追加一个值,则不会超过 s.cap 限制,也就不会重新分配。
	// 通常以 2 倍容量重新分配底层数组。在大大批量添加数据时,建议一一次性分配足足够大大的空
	// 间,以减少内存分配和数据复制开销。或初始化足足够⻓长的 len 属性,改用用索引号进行行操
	// 作。及时释放不再使用的 slice 对象,避免持有过期数组,造成 GC 无法回收

	s4 := make([]int, 0, 1)
	c := cap(s)  // 初始容量是10
	println(c)
	for i := 0; i < 50; i++ {
		s4 = append(s4, i)
		if n := cap(s4); n > c {
			fmt.Printf("cap: %d -> %d\n", c, n)
			c = n
		}
	}
	//
	//cap: 10 -> 16
	//cap: 16 -> 32
	//cap: 32 -> 64
}

func test_copy() {
	// 函数 copy 在两个 slice 间复制数据,复制长度以 len 小的为准。两个 slice 可指向同一
	// 底层数组,允许元素区间重叠。
	data := [...]int{0, 1, 2, 3, 4, 5, 6, 7, 8, 9}
	s := data[8:]
	s2 := data[:5]
	copy(s2, s)
	// dst:s2, src:s
	fmt.Println(s2)
	fmt.Println(data)
	// [8 9 2 3 4]
	// [8 9 2 3 4 5 6 7 8 9]

	// 应及时将所需数据 copy 到较小的 slice,以便释放超大号底层数组内存。
}

func test_map() {
	// 引用类型,哈希表。键必须是支持相等运算符 (==、!=) 类型,比如 number、string、
	// pointer、array、struct,以及对应的 interface。值可以是任意类型,没有限制。
	m := map[int]struct {
		name string
		age int
	}{
		1: {"user1", 10},
		2: {"user2", 20},
		// 可省略元素类型。
	}
	println(m[1].name)
	// 预先给 make 函数一个合理元素数量参数,有助于提升性能。因为事先申请一大块内存, 可避免后续操作时频繁扩张。
	m2 := make(map[string]int, 1000)
	fmt.Println(m2)

	// 常见操作:
	m3 := map[string]int {
		"a": 1,
	}

	// 判断 key 是否存在。
	if v, ok := m3["a"]; ok {
		println(v)
	}

	// 对于不存在的 key,直接返回 \0,不会出错。
	fmt.Println(m3["c"])  // 0

	// 新增或修改
	m3["b"] = 2  // 新增或修改

	// 删除。如果 key 不存在,不会出错。
	delete(m3, "c")

	// 获取键值对数量。cap 无效
	println(len(m3))

	// 迭代,可仅返回 key。随机顺序返回,每次都不相同。
	for k, v := range m3 {
		println(k, v)
	}

	// 从 map 中取回的是一个 value 临时复制品,对其成员的修改是没有任何意义的。
	// 当 map 因扩张而重新哈希时,各键值项存储位置都会发生改变。 因此,map
	// 被设计成 not addressable。 类似 m[1].name 这种期望透过原 value
	// 指针修改成员的行为自然会被禁止。
	type user struct{ name string }
	m4 := map[int]user{
		1: {"user1"},
	}
	// m4[1].name = "Tom" // Error: cannot assign to m[1].name
	// 正确做法是完整替换 value 或使用指针。
	u := m4[1]
	u.name = "Tom"
	m4[1] = u

	m5 := map[int]*user{
		1 : &user{"user1"},
	}
	m5[1].name = "jack"  // 返回的是指针复制品。透过指针修改原对象是允许的
}

func test_strut() {
	// 值类型,赋值和传参会复制全部内容。可用用 "_" 定义补位字段,支支持指向自自身身类型的指针成员。
	type Node struct {
		_ int
		id int
		data *byte
		next *Node
	}

	n1 := Node{
		id: 1,
		data: nil,
	}
	n2 := Node{
		id: 2,
		data: nil,
		next: &n1,
	}
	fmt.Println(n2)

	// 顺序初始化必须包含全部字段,否则会出错。
	type User struct {
		name string
		age int
	}

	u1 := User{"Tom", 20}
	// u2 := User{"Tom"}  // too few values in struct initializer
	fmt.Println(u1)

	// 支持匿名结构,可用作结构成员或定义变量。
	type File struct {
		name string
		size int
		attr struct{
			perm int
			owner int
		}
	}

	f := File{
		name: "test.txt",
		size: 1025,
	}
	f.attr.owner = 1
	f.attr.perm = 0755
	fmt.Println(f)
	var attr = struct {
		perm int
		owner int
	}{2, 0755}

	f.attr = attr
	fmt.Println(f)

	// 可定义字段标签,用反射读取,标签是类型的组成部分
	var u2 struct{ name string `username`}
	fmt.Println(u2)

	// 空结构 "节省" 内存,比如用用来实现 set 数据结构,或者实现没有 "状态" 只有方法的 "静态类"。
	var null struct{}
	set := make(map[string]struct{})
	set["a"] = null

}

func test_struct_anonymous() {
	// 匿名字段不过是一种语法糖,从根本上说,就是一个与成员类型同名 (不含包名) 的字段。被匿名嵌入的可以是任何类型,当然也包括指针。

	type User struct {
		name string
	}
	type Manager struct {
		User
		title string
	}

	m := Manager {
		User: User{"tom"},  // 匿名字段的显式字段名,和类型名相同。
		title: "administrator",
	}
	fmt.Println(m)
	// 可以像普通字段那样访问匿名字段成员,编译器从外向内逐级查找所有层次的匿名字段, 直到发现目标或出错。
	// 外层同名字段会遮蔽嵌入字段成员,相同层次的同名字段也会让编译器无所适从。解决方法是使用显式字段名。
	// 不能同时嵌入入某一一类型和其指针类型,因为它们名字相同。
}

func test_struct_object() {
	// 面面向对象三大大特征里里,Go 仅支支持封装,尽管匿名字段的内存布局和行行为类似继承。没有 class 关键字,没有继承、多态等等。
	type User struct {
		id int
		name string
	}

	type Manager struct {
		User
		title string
	}

	m := Manager{User{1, "Tom"}, "Administrator"}
	// var u User = m  // Error: cannot use m (type Manager) as type User in assignment   没有继承,自自然也不会有多态。
	var u User = m.User  // 同类型拷贝
	fmt.Println(u)
}





























