package user

import (
	"github.com/gin-gonic/gin"
	"github.com/lexkong/log"
	"github.com/lexkong/log/lager"
	"apiserver/util"
	"strconv"
	"apiserver/model"
	. "apiserver/handler"
	"apiserver/pkg/errno"
)

func Update(c *gin.Context) {
	log.Info("Update function called.", lager.Data{"X-Request-Id": util.GetReqId(c)})
	userId, _ := strconv.Atoi(c.Param("id"))

	u := &model.UserModel{}
	// model.DB.Self.First(u)
	if err := c.Bind(u); err != nil {
		SendResponse(c, errno.ErrBind, nil)
		return
	}

	u.Id = uint64(userId)

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

	// 保存
	if err := u.Update(); err != nil {
		SendResponse(c, errno.ErrDatabase, nil)
		return
	}

	SendResponse(c, nil, nil)
}
