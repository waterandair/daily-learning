package model

import (
	"github.com/spf13/viper"
	"fmt"
	"apiserver/pkg/auth"
	validator "gopkg.in/go-playground/validator.v9"
)

type UserModel struct {
	BaseModel
	Username string `json:"username" gorm:"column:username;not null" binding:"required" validate:"min=1,max=32"`
	Password string `json:"password" gorm:"column:password;not null" binding:"required" validate:"min=5,max=128"`
}

func (u *UserModel) TableName() string {
	return "tb_users"
}

// 创建用户
func (u *UserModel) Create() error {
	return DB.Self.Create(&u).Error
}

// 更新用户信息
func (u *UserModel) Update() error {
	//return DB.Self.Model(u).Omit("createdAt", "id").Updates(u).Error
	 return DB.Self.Omit("createdAt").Save(u).Error
}

// 获取用户信息
func GetUser(username string) (*UserModel, error)  {
	u := &UserModel{}
	d := DB.Self.Where("username = ?", username).First(&u)
	return u, d.Error
}

// 用户列表
func ListUser(username string, offset, limit int)([]*UserModel, uint64, error) {
	if limit == 0 {
		limit = viper.GetInt("default_limit")
	}

	users := make([]*UserModel, 0)
	var count uint64

	where := fmt.Sprintf("username like '%%%s%%'", username)
	if err := DB.Self.Model(&UserModel{}).Where(where).Count(&count).Error; err != nil {
		return users, count, err
	}

	if err := DB.Self.Where(where).Offset(offset).Limit(limit).Order("id desc").Find(&users).Error; err != nil {
		return users, count, err
	}

	return users, count, nil
}

// 删除用户
func DeleteUser(id uint64) error {
	user := UserModel{}
	user.BaseModel.Id = id
	return DB.Self.Delete(&user).Error
}

// 加密密码
func (u *UserModel) Encrypt() (err error) {
	u.Password, err = auth.Encrypt(u.Password)
	return
}

// 校验密码
func (u *UserModel) Compare(pwd string) (err error) {
	err = auth.Compare(u.Password, pwd)
	return
}

// 参数校验
func (u *UserModel) Validate() error {
	validate := validator.New()
	return validate.Struct(u)
}