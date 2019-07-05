package weibo

import (
	"time"
)

type User struct {
	ID        uint64    `json:"id"`
	Name      string    `json:"name"`
	Password  string    `json:"password"`
	Email     string    `json:"email"`
	CreatedAt time.Time `json:"created_at"`
	UpdatedAt time.Time `json:"updated_at"`
}

type UserService interface {
	// 添加记录
	Create(user *User) error
	// 根据用户名查询用户
	FindById(id uint64) (*User, error)
	// 根据用户名查询用户
	FindByName(name string) (*User, error)
	// 根据邮箱地址查询用户
	FindByEmail(name string) (*User, error)
	// 对密码字段加密
	Encrypt(user *User) error
}
