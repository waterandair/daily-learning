package main

import (
	"encoding/json"
	"fmt"
)

func main() {
	// 反序列化JSON编码的data，并将结果存储到指向v的指针
	var data = []byte(`[
		{"Name": "Platypus", "Order": "Monotremata"},
		{"Name": "Quoll",    "Order": "Dasyuromorphia"}
	]`)
	type Value struct {
		Name  string
		Order string
	}
	var v []Value
	err := json.Unmarshal(data, &v)
	if err != nil {
		fmt.Println("error:", err)
	}
	fmt.Printf("%+v", v)
}

