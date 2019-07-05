package unit

import (
	"github.com/go-redis/redis"
)

/* 打开 Redis */
func NewRedisConn() *redis.Client {
	var redisClient = redis.NewClient(&redis.Options{
		Addr:     "localhost:6379",
		Password: "",
		DB:       0,
	})
	return redisClient
}
