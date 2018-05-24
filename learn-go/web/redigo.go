package main

import (
	"github.com/garyburd/redigo/redis"
	"time"
	"os"
	"os/signal"
	"syscall"
	"fmt"
)

var (
	Pool *redis.Pool
)

func init() {
	redisHost := "6379"
	Pool = NewPool(redisHost)
	close()
}

func NewPool(server string) *redis.Pool {
	return &redis.Pool{
		// 最大空闲数
		MaxIdle: 3,
		// 空闲连接的超时时间
		IdleTimeout: 240*time.Second,

		Dial: func() (redis.Conn, error) {
			c, err := redis.Dial("tcp", server)
			if err != nil {
				return nil, err
			}
			return c, err
		},

		TestOnBorrow: func(c redis.Conn, t time.Time) error {
			_, err := c.Do("PING")
			return err
		},
	}
}

func close() {
	// Go信号通知通过向一个channel发送``os.Signal`来实现。
	// 创建一个channel来接受这些通知
	c := make(chan os.Signal, 1)
	// `signal.Notify`在给定的channel上面注册该channel 可以接受的信号
	signal.Notify(c, os.Interrupt)
	signal.Notify(c, syscall.SIGTERM)
	signal.Notify(c, syscall.SIGKILL)
	// goroutine阻塞等待信号的到来，当信号到来的时候，输出该信号，然后通知程序可以结束了
	go func() {
		<-c
		Pool.Close()
		os.Exit(0)
	}()
}

func Get(key string) ([]byte, error) {
	conn := Pool.Get()
	defer conn.Close()

	var data []byte
	data, err := redis.Bytes(conn.Do("GET", key))
	if err != nil {
		return  data, fmt.Errorf("error get key %s: %v", key, err)
	}
	return data, err
}



