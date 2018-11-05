package controllers

import (
	"log"
	"net/http"
	"strconv"

	"weibo"
	"weibo/pkg/errno"

	"github.com/labstack/echo"
)

// 点赞模块控制器
type LikeController struct {
	ls weibo.LikeService
}

// 消息列表响应
type messageResponse struct {
	Data []*weibo.Like
}

/* 新建控制器 */
func NewLikeController(ls weibo.LikeService) *LikeController {
	return &LikeController{
		ls: ls,
	}
}

/* 点赞 post 请求 */
func (c *LikeController) Like(ctx echo.Context) error {
	// 点赞者
	user := ctx.Get("user").(*weibo.User)
	fromUserId := user.ID
	fromUserName := user.Name

	// 被点赞者
	toUserId := ctx.FormValue("to_user_id")
	toIdUint64, err := strconv.ParseUint(toUserId, 10, 64)
	failOnError(err, "")

	// 微博 id
	postId := ctx.FormValue("post_id")
	postIdUint64, err := strconv.ParseUint(postId, 10, 64)
	failOnError(err, "")

	likeMessage := &weibo.Like{
		FromUserId:   fromUserId,
		FromUserName: fromUserName,
		ToUserId:     toIdUint64,
		PostId:       postIdUint64,
	}

	// 异步发送消息，若失败重试两次
	go func() {
		for i := 3; i > 0; i-- {
			// 发送消息
			res, err := c.ls.SendMessage(likeMessage)

			if res.Res == true {
				return
			} else {
				log.Fatalf("grpc likeServive Client sendMessage failed. " + err.Error())
			}

		}
	}()

	response := MakeResponse(err, likeMessage)
	return ctx.JSON(http.StatusOK, response)
}

/* 获取未读消息 get 请求*/
func (c *LikeController) Message(ctx echo.Context) error {
	// 当前用户
	user := ctx.Get("user").(*weibo.User)

	nums := ctx.Param("nums")
	numsUint, err := strconv.ParseUint(nums, 10, 64)
	if err != nil {
		ctx.JSON(http.StatusOK, errno.New(errno.ErrValidation, err))
	}

	// 获取未读消息
	messages, err := c.ls.Messages(user.ID, numsUint)
	if err != nil {
		return ctx.JSON(http.StatusOK, errno.New(errno.ErrDatabase, err))
	}

	response := messageResponse{Data: messages}
	return ctx.Render(http.StatusOK, "messages.html", response)
}

/* 消费点赞消息队列 */
func (c *LikeController) ConsumeMessage() {
	c.ls.ConsumeMessage()
}
