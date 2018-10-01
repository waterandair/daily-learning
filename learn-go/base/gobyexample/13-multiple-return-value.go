package main

import "fmt"

func vals () (int, int) {
	return 2, 3
}

func main() {
	a, b := vals()
	fmt.Println(a)  // 2
	fmt.Println(b)  // 3

	_, c := vals()
	fmt.Println(c)  // 3
}
