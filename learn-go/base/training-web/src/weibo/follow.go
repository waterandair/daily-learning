package weibo

import (
	"time"
)

type Follow struct {
	Id             string    `json:"id"`
	UserId         uint64    `json:"user_id"`
	FollowedUserId uint64    `json:"followed_user_id"`
	CreatedAt      time.Time `json:"created_at"`
	UpdatedAt      time.Time `json:"updated_at"`
}

type FollowService interface {
	// 关注
	Follow(follow *Follow) error
	// 检查是否已关注
	CheckFollowed(userId, followedUserId uint64) bool
	// 获取关注数
	GetFollowCount(userId uint64) (uint64, error)
	// 获取粉丝数
	GetFansCount(userId uint64) (uint64, error)
}
