package services

import (
	"context"
	"encoding/json"
	"log"
	"strconv"
	"time"

	"weibo"
	"weibo/proto/like"
	"weibo/unit"

	"github.com/go-redis/redis"
	"github.com/jinzhu/gorm"
)

/* 点赞服务 */
type LikeService struct {
	db             *gorm.DB
	redis          *redis.Client
	grpcLikeClient like.LikeServiceClient
	RabbitMq       *unit.RabbitMqClient
}

/* 新建服务 */
func NewLikeService(db *gorm.DB, redis *redis.Client, grpcLikeClient like.LikeServiceClient, rabbitMq *unit.RabbitMqClient) *LikeService {
	return &LikeService{
		db:             db,
		redis:          redis,
		grpcLikeClient: grpcLikeClient,
		RabbitMq:       rabbitMq,
	}
}

/* 点赞 */
func (s *LikeService) Like(like *weibo.Like) error {
	err := s.db.Create(&like).Error
	if err == nil {
		// redis 文章增加点赞数
		s.IncrLikesCountToRedis(like.PostId)
		// redis 增加被点赞人的消息数
		s.IncrMessagesCountToRedis(like.ToUserId)

	}
	return err
}

/* 未读点赞消息列表 */
func (s *LikeService) Messages(toUserId uint64, nums uint64) (messages []*weibo.Like, err error) {
	if err := s.db.Where("to_user_id = ?", toUserId).Limit(nums).Order("id desc").Find(&messages).Error; err != nil {
		return messages, err
	}

	// 重置消息数
	s.ResetMessagesCount(toUserId)
	return messages, nil
}

/* 消息数 */
func (s *LikeService) GetMessagesCount(toUserId uint64) (uint64, error) {
	var count uint64
	count, err := s.GetMessagesCountFromRedis(toUserId)

	return count, err
}

/* 获取微博点赞数 */
func (s *LikeService) GetLikesCount(userId uint64) (uint64, error) {
	var count uint64
	count, err := s.GetLikesCountFromRedis(userId)
	if err == nil {
		return count, err
	}
	err = s.db.Model(&weibo.Like{}).Where("to_user_id = ?", userId).Count(&count).Error
	if err != nil {
		log.Println(err.Error())
	}
	return count, err
}

/* 获取点赞数 */
func (s *LikeService) GetLikesCountFromRedis(postId uint64) (uint64, error) {
	likesCountKey := "post:id:" + strconv.FormatUint(postId, 10) + ":likes"
	s.redis.SetNX(likesCountKey, 0, 0)

	likesCount, err := s.redis.Get(likesCountKey).Uint64()
	if err != nil {
		log.Println(err)
	}

	return likesCount, err
}

/* redis 获取未读点赞消息数 */
func (s *LikeService) GetMessagesCountFromRedis(toUserId uint64) (uint64, error) {
	messagesCountKey := "user:id:" + strconv.FormatUint(toUserId, 10) + ":messages"
	s.redis.SetNX(messagesCountKey, 0, 0)

	messagesCount, err := s.redis.Get(messagesCountKey).Uint64()
	if err != nil {
		log.Println(err)
	}

	return messagesCount, err
}

/* redis 增加消息数 */
func (s *LikeService) IncrMessagesCountToRedis(userId uint64) error {
	fansCountKey := "user:id:" + strconv.FormatUint(userId, 10) + ":messages"
	s.redis.SetNX(fansCountKey, 0, 0)
	if _, err := s.redis.Incr(fansCountKey).Result(); err != nil {
		return err
	}
	return nil
}

/* redis 增加点赞数 */
func (s *LikeService) IncrLikesCountToRedis(postId uint64) error {
	fansCountKey := "user:id:" + strconv.FormatUint(postId, 10) + ":likes"
	s.redis.SetNX(fansCountKey, 0, 0)

	if _, err := s.redis.Incr(fansCountKey).Result(); err != nil {
		return err
	}
	return nil
}

// redis  读取未读消息列表后，重置消息数
func (s *LikeService) ResetMessagesCount(userId uint64) error {
	fansCountKey := "user:id:" + strconv.FormatUint(userId, 10) + ":messages"
	s.redis.SetNX(fansCountKey, 0, 0)
	if _, err := s.redis.Set(fansCountKey, 0, 0).Result(); err != nil {
		return err
	}
	return nil
}

/* 发送点赞消息 grpc 点赞服务 客户端 */
func (s *LikeService) SendMessage(likeMessage *weibo.Like) (*like.Result, error) {
	// grpc 客户端 发送消息
	ctx, cancel := context.WithTimeout(context.Background(), 3*time.Second)
	defer cancel()
	r, err := s.grpcLikeClient.SendMessage(ctx, &like.Like{
		FromUserId:   likeMessage.FromUserId,
		FromUserName: likeMessage.FromUserName,
		ToUserId:     likeMessage.ToUserId,
		PostId:       likeMessage.PostId,
	})

	if err != nil {
		log.Println(err.Error(), "grpc 发送消息失败")
	}
	return r, err
}

/* 消费消息 */

func (s *LikeService) ConsumeMessage() {
	// 读取消息队列
	msgs, err := s.RabbitMq.Channel.Consume(
		s.RabbitMq.Queue.Name, // queue
		"",                    // consumer
		true,                  // auto-ack
		false,                 // exclusive
		false,                 // no-local
		false,                 // no-wait
		nil,                   // args
	)
	if err != nil {
		log.Println("Failed to register a consumer")
	}

	// 创建一个 go channel 用于阻塞，这样就可以不停的读取消息队列
	forever := make(chan bool)

	// 消息队列异步向消费者推送消息，所以消费者读消息的时候用 goroutine 去读
	go func() {
		for d := range msgs {
			var message map[string]interface{}
			if err := json.Unmarshal(d.Body, &message); err != nil {
				panic(err)
			}

			likeMessage := &weibo.Like{
				FromUserId:   uint64(message["fromUserId"].(float64)),
				FromUserName: message["fromUserName"].(string),
				ToUserId:     uint64(message["toUserId"].(float64)),
				PostId:       uint64(message["postId"].(float64)),
			}
			log.Println(likeMessage)

			// 向数据库 likes 表添加记录
			if err := s.Like(likeMessage); err != nil {
				log.Fatalf("consume queue 'like' mysql error: %s", err.Error())
			} else {

				log.Println("consume queue 'like' success")
			}

		}
	}()

	// 一直等待
	<-forever
}
