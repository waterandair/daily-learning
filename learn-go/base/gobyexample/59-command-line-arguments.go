package main

import (
	"fmt"
	"os"
)

//  ./59-command-line-arguments a b c d
func main() {
	argsWithProg := os.Args
	argsWithoutProg := os.Args[1:]

	arg := os.Args[3]

	fmt.Println(argsWithProg)  // [./59-command-line-arguments a b c d]
	fmt.Println(argsWithoutProg)  // [a b c d]
	fmt.Println(arg)  // c
}


