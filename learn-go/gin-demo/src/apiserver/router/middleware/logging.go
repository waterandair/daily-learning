package middleware

import (
	"apiserver/handler"
	"apiserver/pkg/errno"
	"bytes"
	"encoding/json"
	"github.com/gin-gonic/gin"
	"github.com/lexkong/log"
	"github.com/willf/pad"
	"io/ioutil"
	"regexp"
	"time"
)

type bodyLogWriter struct {
	gin.ResponseWriter // 构造HTTP响应
	body               *bytes.Buffer
}

func (w bodyLogWriter) Write(b []byte) (int, error) {
	w.body.Write(b)
	return w.ResponseWriter.Write(b)
}

func Logging() gin.HandlerFunc {
	return func(c *gin.Context) {
		start := time.Now().UTC()
		path := c.Request.URL.Path
		method := c.Request.Method
		ip := c.ClientIP()

		// 只记录 /v1/user 或 /v1/login 的日志
		req := regexp.MustCompile("(/v1/user|/login)") // MustCompile类似Compile但会在解析失败时panic，主要用于全局正则表达式变量的安全初始化。
		if !req.MatchString(path) {
			return
		}

		var bodyBytes []byte
		if c.Request.Body != nil {
			bodyBytes, _ = ioutil.ReadAll(c.Request.Body)
		}

		// http 的请求body在读取过后会被置空,所以要保存到这里
		c.Request.Body = ioutil.NopCloser(bytes.NewBuffer(bodyBytes))

		// 封装 body 和 c.Writer
		blw := &bodyLogWriter{
			body:           bytes.NewBufferString(""),
			ResponseWriter: c.Writer,
		}
		c.Writer = blw

		// 请求前
		c.Next()
		// 请求后

		end := time.Now().UTC()
		latency := end.Sub(start) // 计算响应时间

		code, message := -1, ""
		var resp handler.Response
		if err := json.Unmarshal(blw.body.Bytes(), &resp); err != nil {
			log.Errorf(err, "response body can not Unmarshal to model.Response struct. body: `%s`", blw.body.Bytes())
			code = errno.InternalServerError.Code
			message = err.Error()
		} else {
			code = resp.Code
			message = resp.Message
		}

		log.Infof("%-13s | %-12s | %s %s | {code: %d, message: %s}", latency, ip, pad.Right(method, 5, ""), path, code, message)
	}
}
