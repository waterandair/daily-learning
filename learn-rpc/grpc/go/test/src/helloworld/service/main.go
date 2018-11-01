package main

import (
	"context"
	"github.com/labstack/gommon/log"
	"google.golang.org/grpc"
	"google.golang.org/grpc/examples/helloworld/helloworld"
	"google.golang.org/grpc/reflection"
	"net"
)

const Port  = ":50000"
type server struct {}

func (s *server) SayHello(ctx context.Context, in *helloworld.HelloRequest) (*helloworld.HelloReply, error){
	return &helloworld.HelloReply{
		Message: "Hello" + in.Name,
	}, nil
}

func main() {
	listen, err := net.Listen("tcp", Port)
	if err != nil {
		log.Fatalf("failed to listen: %v", nil)
	}

	s := grpc.NewServer()
	helloworld.RegisterGreeterServer(s, &server{})

	reflection.Register(s)

	if err := s.Serve(listen); err != nil {
		log.Fatalf("failed to serve: %v", err)
	}

}