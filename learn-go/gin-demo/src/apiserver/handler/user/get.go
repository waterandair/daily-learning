package user

import (
	"github.com/gin-gonic/gin"
	"apiserver/model"
	. "apiserver/handler"
	"apiserver/pkg/errno"
)

// 获取用户信息
func Get(c *gin.Context) {
	username := c.Param("username")

	user, err := model.GetUser(username)
	if err != nil {
		SendResponse(c, errno.ErrUserNotFound, nil)
		return
	}

	SendResponse(c, nil , user)
}
