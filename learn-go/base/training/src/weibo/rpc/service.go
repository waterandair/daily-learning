package main

import (
	"context"
	"encoding/json"
	"log"
	"net"

	"weibo/proto/like"
	"weibo/unit"

	"github.com/spf13/viper"
	"github.com/streadway/amqp"
	"google.golang.org/grpc"
	"google.golang.org/grpc/reflection"
)

// rabbitMq 点赞队列
type likeService struct {
	queue   *amqp.Queue
	channel *amqp.Channel
}

/* grpc 点赞服务端发送消息给 rabbitMq 消息队列 */
func (s *likeService) SendMessage(ctx context.Context, in *like.Like) (*like.Result, error) {

	// 返回消息是否发送成功
	res := &like.Result{Res: true}

	// 将消息序列化为 json 格式
	message, err := json.Marshal(in)
	failOnError(err, "json marshal failed")

	// 向 rabbitMq 发送消息
	err = s.channel.Publish(
		"",
		s.queue.Name,
		false,
		false,
		amqp.Publishing{
			ContentType: "text/plain",
			Body:        []byte(message),
		})

	if err != nil {
		res.Res = false
	}
	log.Println(string(message), res)

	return res, err
}

/* 记录错误日志并退出程序 */
func failOnError(err error, msg string) {
	if err != nil {
		log.Fatalf("%s: %s", msg, err)
	}
}

func main() {
	// 初始化配置
	if err := unit.InitConfig(""); err != nil {
		log.Fatal(err)
	}

	// 初始化 rabbitMq 连接
	rabbitMq := unit.NewRabbitMqConn("like")
	defer rabbitMq.Conn.Close()
	defer rabbitMq.Channel.Close()

	// grpc 服务端监听端口
	listen, err := net.Listen("tcp", viper.GetString("grpc_like_host"))
	if err != nil {
		log.Fatalf("grpc LikeService failed to listen: %v", err)
	}

	// 创建 grpc 服务端
	s := grpc.NewServer()
	like.RegisterLikeServiceServer(s, &likeService{queue: rabbitMq.Queue, channel: rabbitMq.Channel})
	reflection.Register(s)

	if err := s.Serve(listen); err != nil {
		log.Fatalf("grpc LikeService failed to serve: %v", err)
	}

}
