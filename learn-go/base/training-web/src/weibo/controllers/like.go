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
	Messages []*weibo.Like  `json:"messages"`
}

/* 新建控制器 */
func NewLikeController(ls weibo.LikeService) *LikeController {
	return &LikeController{
		ls: ls,
	}
}

type LikeRequest struct {
	ToUserId uint64 `json:"to_user_id"`
	PostId  uint64  `json:"post_id"`
}

/* 点赞 post 请求 */
func (c *LikeController) Like(ctx echo.Context) error {

	log.Println("-------sendmessage ------ ")
	// 点赞者
	user := ctx.Get("user").(*weibo.User)
	fromUserId := user.ID
	fromUserName := user.Name

	var r LikeRequest
	if err := ctx.Bind(&r); err != nil {
		response := MakeResponse(err, nil)
		return ctx.JSON(http.StatusOK, response)
	}
	//err := ctx.Bind(&r)
	//response := MakeResponse(err, nil)
	//return ctx.JSON(http.StatusOK, response)

	likeMessage := &weibo.Like{
		FromUserId:   fromUserId,
		FromUserName: fromUserName,
		ToUserId:     r.ToUserId,
		PostId:       r.PostId,
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

	response := MakeResponse(nil, likeMessage)
	return ctx.JSON(http.StatusOK, response)
}

/* 获取未读消息 get 请求*/
func (c *LikeController) Message(ctx echo.Context) error {
	// 当前用户
	user := ctx.Get("user").(*weibo.User)

	nums := ctx.Param("nums")
	numsUint, err := strconv.ParseUint(nums, 10, 64)
	if err != nil {
		response := MakeResponse(errno.New(errno.ErrValidation, err), nil)
		return ctx.JSON(http.StatusOK, response)
	}

	// 获取未读消息
	messages, err := c.ls.Messages(user.ID, numsUint)
	if err != nil {
		response := MakeResponse(errno.New(errno.ErrValidation, err), nil)
		return ctx.JSON(http.StatusOK, response)
	}

	data := messageResponse{Messages: messages}
	response := MakeResponse(nil, data)
	return ctx.JSON(http.StatusOK, response)
}

/* 消费点赞消息队列 */
func (c *LikeController) ConsumeMessage() {
	c.ls.ConsumeMessage()
}
