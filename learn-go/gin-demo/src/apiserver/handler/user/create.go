package user

import (
	. "apiserver/handler"
	"apiserver/model"
	"apiserver/pkg/errno"
	"github.com/gin-gonic/gin"
	"net/http"
)

// 创建用户
func Create(c *gin.Context) {
	var r CreateRequest

	// 解析参数到 CreateRequest
	if err := c.Bind(&r); err != nil {
		c.JSON(http.StatusOK, errno.ErrBind)
		return
	}

	u := model.UserModel{
		Username: r.Username,
		Password: r.Password,
	}

	// 校验参数
	if err := u.Validate(); err != nil {
		SendResponse(c, errno.ErrValidation, nil)
		return
	}

	// 加密密码
	if err := u.Encrypt(); err != nil {
		SendResponse(c, errno.ErrEncrypt, nil)
		return
	}

	// 存入数据库
	if err := u.Create(); err != nil {
		SendResponse(c, errno.ErrDatabase, nil)
		return 
	}

	// 响应
	resp := CreateResponse{
		Username: r.Username,
	}

	SendResponse(c, nil, resp)
}
