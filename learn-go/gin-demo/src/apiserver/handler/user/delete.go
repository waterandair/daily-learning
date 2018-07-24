package user

import (
	"github.com/gin-gonic/gin"
	"strconv"
	"apiserver/model"
	. "apiserver/handler"
	"apiserver/pkg/errno"
)

// 软删除一个用户
func Delete(c *gin.Context) {
	UserId, _ := strconv.Atoi(c.Param("id"))
	if err := model.DeleteUser(uint64(UserId)); err != nil {
		SendResponse(c, errno.ErrDatabase, nil)
		return
	}

	SendResponse(c, nil, nil)
}
