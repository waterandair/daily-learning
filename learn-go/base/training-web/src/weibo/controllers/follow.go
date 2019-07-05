package controllers

import (
	"log"
	"net/http"
	"weibo"
	"weibo/pkg/errno"

	"github.com/labstack/echo"
)

// 关注模块控制器结构体
type FollowController struct {
	fs weibo.FollowService
}

/* 创建关注模块控制器 */
func NewFollowController(fs weibo.FollowService) *FollowController {
	return &FollowController{
		fs: fs,
	}
}

// 关注请求结构体
type FollowRequest struct {
	FollowedUserId uint64 `json:"followed_user_id"`
}

/* 关注 post 请求 */
func (c *FollowController) Follow(ctx echo.Context) error {
	// 当前用户
	user := ctx.Get("user").(*weibo.User)

	var r FollowRequest
	// 被关注的用户
	if err := ctx.Bind(&r); err != nil {
		return ctx.JSON(http.StatusOK, MakeResponse(err, nil))
	}


	// 验证是否已经关注过
	if c.fs.CheckFollowed(user.ID, r.FollowedUserId) == false {
		response := MakeResponse(errno.New(errno.ErrDuplicateFollow, nil), "您已关注过该用户")
		return ctx.JSON(http.StatusOK, response)
	}

	follow := weibo.Follow{
		UserId:         user.ID,
		FollowedUserId: r.FollowedUserId,
	}
	log.Println("-----follow-----")

	// 添加数据库记录 增加 redis 的关注数和粉丝数
	if err := c.fs.Follow(&follow); err != nil {
		response := MakeResponse(errno.New(errno.ErrDatabase, err), nil)
		return ctx.JSON(http.StatusOK, response)
	}

	response := MakeResponse(nil, nil)
	return ctx.JSON(http.StatusOK, response)
}
