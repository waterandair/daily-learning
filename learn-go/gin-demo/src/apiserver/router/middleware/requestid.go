package middleware

import (
	"github.com/gin-gonic/gin"
	"github.com/satori/go.uuid"
)

// 请求id中间件
func RequestId() gin.HandlerFunc {
	return func(c *gin.Context) {
		requestId := c.Request.Header.Get("X-Request-Id")

		// 如果请求header中没有请求id, 就生成 uuid
		if requestId == "" {
			u4, _ := uuid.NewV4()
			requestId = u4.String()
		}

		c.Set("X-Request-Id", requestId)

		// 给响应header中添加 请求id
		c.Writer.Header().Set("X-Request-Id", requestId)
		c.Next()
	}
}
