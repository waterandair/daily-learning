package main
// 表达式
import (
	"fmt"
	"strconv"
)

func main() {
	// test_2_4_for()
	// test_2_4_range()
	// test_2_4_switch()

	// goto break continue
	test_2_4_5()

}

func test_2_4_if() {
	// 可省略条件表达式括号。
	// 支持初始化语句,可定义代码块局部变量。
	// 代码块左大括号必须在条件表达式尾部。
	// 不支持三元操作符
}

func test_2_4_for() {
	// 支持三种循环方式
	s := "abc"

	for i,n := 0, len(s); i < n; i++ {
		fmt.Println(string(s[i]))
	}

	n := len(s)
	for n > 0 {
		n--
		fmt.Println(string(s[n]))
	}

	// 死循环
	//for {
	//	fmt.Println(s)
	//}
}

func test_2_4_range() {
	s := "abc"

	for i := range s {
		fmt.Println(s[i])
	}

	// 忽略索引
	for _, c := range s {
		fmt.Println(c)
	}

	for range s {
		fmt.Println("忽略所有值,仅迭代")
	}

	m := map[string]int{"a": 1, "b": 2}
	for k, v := range m {
		fmt.Println(k, v)
	}

	// 注意,range 会复制对象 (array)。
	a := [3]int{0, 1, 2}

	for i, v := range a {  // index、value 都是从复制品中取出。

		// 修改原数组
		if i == 0 {
			a[1], a[2] = 999, 999
			fmt.Println(a)   // [0 999 999]
		}

		// 这里的 v 是复制品, 依然是 0, 1, 2
		a[i] = v + 100
		println(i, v)
	}

	fmt.Println(a)  // [100 101 102]

	// 建议改用引用类型(slice),其底层数据不会被复制。
	s2 := []int{1, 2, 3, 4, 5}

	for i, v := range s2 {
		if i == 0 {
			// 对 slice 的修改,不会影响 range。
			//s2 = s2[:3]
			s2[2] = 100
		}
		println(i, v)
	}
}

func test_2_4_switch() {
	// 分支表达式可以是任意类型,不限于常量。可省略 break,默认自动终止。
	x := []int{1, 2, 3}
	i := 2

	switch i {
		case x[1]:
			fmt.Println("a")
		case 1, 3 :
			fmt.Println("b")
		default:
			fmt.Println("c")
	}

	// 如需要继续下一分支,可使用 fallthrough,但不再判断条件。
	x2 := 10
	switch x2 {
	case 10:
		fmt.Println("a")
		fallthrough
	case 0:
		fmt.Println("b")
	}

	// 省略条件表达式,可当 if...else if...else 使用
	switch {
	case x[1] > 0:
		fmt.Println("a")
	case x[1] < 0:
		println("b")
	default:
		fmt.Println("c")
	}

	// 带初始化语句
	switch i := x[2]; {
	case i > 0:
		fmt.Println("a")
	case i < 0:
		fmt.Println("b")
	default:
		println("c")
	}
}

func test_2_4_5() {
	var i int

	// 支持在函数内 goto 跳转。标签名区分大小写,未使用标签引发错误。
	for {
		println(i)
		i++
		if i > 2 { goto BREAK}
	}

	BREAK:
		println("break")


	// 配合标签,break 和 continue 可在多级嵌套循环中跳出。
	L1:
		for x := 0; x < 3; x++ {
	L2:
			for y := 0; y < 5; y++ {
				if y > 2 {continue L2}
				if x > 1 {break L1}

				print(strconv.Itoa(x), ":", y, " ")
			}
			println()
		}

	// break 可用用于 for、switch、select,而而 continue 仅能用用于 for 循环。
}


