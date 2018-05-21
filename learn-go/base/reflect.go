package main

import "reflect"

var x float64 = 3.4
var y float64 = 3.4

func main() {
	v := reflect.ValueOf(x)
	fmt.Println(v.Type())
	fmt.Println(v.Kind() == reflect.Float64)
	fmt.Println(v.Float())
	// v.SetFloat(5.0)

	p := reflect.ValueOf(&y)
	v2 := p.Elem()
	v2.SetFloat(7.1)
	fmt.Println(y)
}
