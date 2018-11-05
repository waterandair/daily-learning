package services

import (
	"weibo"
	"weibo/pkg/auth"

	"github.com/jinzhu/gorm"
)

// 用户模块 服务
type UserService struct {
	db *gorm.DB
}

/* 新建服务 */
func NewUserService(db *gorm.DB) *UserService {
	return &UserService{
		db: db,
	}
}

/* 用户注册 */
func (u *UserService) Create(user *weibo.User) error {
	return u.db.Create(&user).Error
}

/* 根据id查找用户 */
func (u *UserService) FindById(id uint64) (*weibo.User, error) {
	user := &weibo.User{}
	res := u.db.Where("id = ?", id).First(&user)
	return user, res.Error
}

/* 根据用户名查找用户 */
func (u *UserService) FindByName(name string) (*weibo.User, error) {
	user := &weibo.User{}
	res := u.db.Where("name = ?", name).First(&user)
	return user, res.Error
}

/* 根据 email 查找用户 */
func (u *UserService) FindByEmail(email string) (*weibo.User, error) {
	user := &weibo.User{}
	res := u.db.Where("email = ?", email).First(&user)
	return user, res.Error
}

/* 加密密码 */
func (u *UserService) Encrypt(user *weibo.User) (err error) {
	user.Password, err = auth.Encrypt(user.Password)
	return err
}
