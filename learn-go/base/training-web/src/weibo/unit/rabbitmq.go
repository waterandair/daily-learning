package unit

import (
	"log"

	"github.com/spf13/viper"
	"github.com/streadway/amqp"
)

type RabbitMqClient struct {
	Conn    *amqp.Connection
	Channel *amqp.Channel
	Queue   *amqp.Queue
}

/* 初始化 Grpc 客户端 */
func NewRabbitMqConn(queueName string) *RabbitMqClient {

	// 连接 RabbitMq
	conn, err := amqp.Dial(viper.GetString("rabbitMq_host"))
	if err != nil {
		log.Fatalf("did not connect: %v", err)
	}

	ch, err := conn.Channel()
	if err != nil {
		log.Fatalf("did not connect: %v", err)
	}

	// 声明队列，因为消费者可能先于生产者运行
	q, err := ch.QueueDeclare(
		queueName, // name
		false,     // durable
		false,     // delete when usused
		false,     // exclusive
		false,     // no-wait
		nil,       // arguments
	)

	if err != nil {
		log.Fatalf("did not connect: %v", err)
	}

	return &RabbitMqClient{
		Conn:    conn,
		Channel: ch,
		Queue:   &q,
	}
}
