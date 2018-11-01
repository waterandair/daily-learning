package main

import (
	"context"
	"github.com/labstack/gommon/log"
	"google.golang.org/grpc"
	"google.golang.org/grpc/examples/helloworld/helloworld"
	"os"
	"time"
)

const(
	Address = "localhost:50000"
	DefaultName = "world"
)

func main() {
	conn, err := grpc.Dial(Address, grpc.WithInsecure())
	if err != nil {
		log.Fatalf("did not connect: %v", err)
	}
	defer conn.Close()

	c := helloworld.NewGreeterClient(conn)

	name := DefaultName
	if len(os.Args) > 1 {
		name = os.Args[1]
	}

	ctx, cancel := context.WithTimeout(context.Background(), time.Second)
	defer cancel()
	r, err := c.SayHello(ctx, &helloworld.HelloRequest{Name:name})

	if err != nil {
		log.Fatalf("could not greet: %v", err)
	}

	time.Sleep(3*time.Second)
	log.Printf("reply: %s", r.Message)
}
