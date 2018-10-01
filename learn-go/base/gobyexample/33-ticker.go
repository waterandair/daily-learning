package main

import (
	"fmt"
	"time"
)

func main() {
	ticker := time.NewTicker(500 * time.Microsecond)
	go func() {
		for t := range ticker.C {
			fmt.Println("Tick at ", t)
		}
	}()

	time.Sleep(1600 * time.Microsecond)
	ticker.Stop()
	fmt.Println("Ticker stopped")
}
