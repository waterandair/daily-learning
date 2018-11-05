package unit

import (
	"log"

	"weibo/proto/like"

	"github.com/spf13/viper"
	"google.golang.org/grpc"
)

type GrpcClient struct {
	GrpcConn   *grpc.ClientConn
	GrpcClient like.LikeServiceClient
}

/* 初始化 Grpc 客户端 */
func NewGrpcLikeConn() *GrpcClient {

	// 连接 grpc 服务端
	conn, err := grpc.Dial(viper.GetString("grpc_like_host"), grpc.WithInsecure())
	if err != nil {
		log.Fatalf("did not connect: %v", err)
	}

	// 创建客户端
	client := like.NewLikeServiceClient(conn)

	return &GrpcClient{
		GrpcConn:   conn,
		GrpcClient: client,
	}
}
