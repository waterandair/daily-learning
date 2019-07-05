package weibo

import (
	"time"
	"weibo/proto/like"
)

type Like struct {
	Id           uint64    `json:"id"`
	FromUserId   uint64    `json:"from_user_id"`
	FromUserName string    `json:"from_user_name"`
	ToUserId     uint64    `json:"to_user_id"`
	PostId       uint64    `json:"post_id"`
	CreatedAt    time.Time `json:"created_at"`
	UpdatedAt    time.Time `json:"updated_at"`
}

type LikeService interface {
	// 点赞
	Like(like *Like) error
	// 未读消息列表
	Messages(toUserId uint64, nums uint64) (messages []*Like, err error)
	// 获取文章点赞数
	GetLikesCount(userId uint64) (uint64, error)
	// 获取消息数
	GetMessagesCount(userId uint64) (uint64, error)
	// 发消息
	SendMessage(likeMessage *Like) (*like.Result, error)
	// 消费消息
	ConsumeMessage()
}
