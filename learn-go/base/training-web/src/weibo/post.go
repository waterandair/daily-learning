package weibo

import (
	"time"
)

type Post struct {
	ID        uint64    `json:"id"`
	UserId    uint64    `json:"user_id"`
	UserName  string    `json:"user_name"`
	Content   string    `json:"content"`
	CreatedAt time.Time `json:"created_at"`
	UpdatedAt time.Time `json:"updated_at"`
}

type PostService interface {
	// 获取微博总数
	CountAll() uint64
	// 写微博
	Create(post *Post) error
	// 微博列表-首页
	List(offset, limit uint64) (posts []Post, err error)
	// 获取个人微博数
	GetPostsCountByUserId(userId uint64) (uint64, error)
}
