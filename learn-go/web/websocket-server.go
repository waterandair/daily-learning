package main

import (
	"fmt"
	"log"
	"net/http"
	"golang.org/x/net/websocket"
)

func Echo(ws *websocket.Conn) {
	var err error

	for {
		var reply string
		if err = websocket.Message.Receive(ws, &reply); err != nil {
			fmt.Println("Can't receive")
			break
		}

		for _, v := range ws.Config().Protocol {
			switch v {
				case "zj":
					fmt.Println("zj")
				default:
					fmt.Println("default")
			}
		}

		fmt.Println("Received back from client: " + reply)

		msg := "Received:  " + reply
		fmt.Println("Sending to client: " + msg)
		if err = websocket.Message.Send(ws, msg); err != nil {
			fmt.Println("Can't send")
			break
		}
	}
}

func main() {
	http.Handle("/", websocket.Handler(Echo))
	if err := http.ListenAndServe(":1234", nil); err != nil {
		log.Fatal("ListenAndServe:", err)
	}
}