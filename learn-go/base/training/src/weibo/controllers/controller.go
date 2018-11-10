package controllers

import (
	"github.com/labstack/echo"
	"log"

	"weibo/pkg/errno"
)

/* 统一响应结构 */
type Response struct {
	Code    int         `json:"code"`
	Message string      `json:"message"`
	Data    interface{} `json:"data"`
}

/* 统一响应 */
func MakeResponse(err error, data interface{}) Response {

	code, message := errno.DecodeErr(err)
	return Response{
		Code:    code,
		Message: message,
		Data:    data,
	}
}

/* 记录错误日志并退出 */
func failOnError(err error, msg string) {
	if err != nil {
		log.Fatalf("%s: %s", msg, err)
	}
}

func SendResponse(err error, data interface{}, ctx echo.Context) Response {
	// 设置响应 header

	code, message := errno.DecodeErr(err)
	return Response{
		Code:    code,
		Message: message,
		Data:    data,
	}
}


/* 统一响应 */
func MakeResponse2(err error, data interface{}, ctx echo.Context) (Response, echo.Context) {

	ctx.Response().Header().Set("Access-Control-Allow-Credentials", "true")
	ctx.Response().Header().Set("Access-Control-Allow-Origin", "http://localhost:8080") //允许访问所有域
	ctx.Response().Header().Add("Access-Control-Allow-Headers", "Content-Type")       //header的类型
	ctx.Response().Header().Set("content-type", "application/json")                   //返回数据格式是json

	code, message := errno.DecodeErr(err)
	return Response{
		Code:    code,
		Message: message,
		Data:    data,
	}, ctx
}