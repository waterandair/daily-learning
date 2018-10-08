package main

import (
	"fmt"
	"math/rand"
	"time"
)

// math/rand 提供伪随机数生成

func main() {
	// [0, 100)
	fmt.Print(rand.Intn(100), ",")
	fmt.Print(rand.Intn(100))
	fmt.Println()

	// [0.0, 1.0)
	fmt.Println(rand.Float64())

	fmt.Print((rand.Float64() * 5) + 5, ",")
	fmt.Print((rand.Float64() * 5) + 5)
	fmt.Println()

	// 如果需要产生不同的，可以提供一个变化的种子
	s1 := rand.NewSource(time.Now().UnixNano())
	r1 := rand.New(s1)

	fmt.Print(r1.Intn(100), ",")
	fmt.Print(r1.Intn(100))
	fmt.Println()

	// 种子相同，产生的随机数也总是相同
	s2 := rand.NewSource(42)
	r2 := rand.New(s2)
	fmt.Print(r2.Intn(100), ",")
	fmt.Print(r2.Intn(100))
	fmt.Println()
	s3 := rand.NewSource(42)
	r3 := rand.New(s3)
	fmt.Print(r3.Intn(100), ",")
	fmt.Print(r3.Intn(100))


}
