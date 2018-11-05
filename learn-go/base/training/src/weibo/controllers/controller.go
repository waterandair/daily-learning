package controllers

import (
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
