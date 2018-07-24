package util

import (
	"github.com/teris-io/shortid"
	"github.com/gin-gonic/gin"
)

func GenShortId() (string, error) {
	return shortid.Generate()
}

func GetReqId(c *gin.Context) string {
	v, ok := c.Get("X-Request-Id")
	if !ok {
		return ""
	}
	if requestId, ok := v.(string); ok {
		return requestId
	}
	return ""
}
