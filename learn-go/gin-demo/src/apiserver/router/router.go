package router

import (
	"github.com/gin-gonic/gin"
	"apiserver/router/middleware"
	"net/http"
	"apiserver/handler/sd"
	"apiserver/handler/user"
)

// 加载 middlewares, routes, handlers
func Load(g *gin.Engine, mw ...gin.HandlerFunc) *gin.Engine {
	// middlewares
	g.Use(gin.Recovery())  // 恢复所有 panic 且返回 500, 保护程序不会停止运行
	g.Use(middleware.Nochche)  // 强制浏览器不使用缓存
	g.Use(middleware.Options)  // 浏览器跨域 options 请求设置
	g.Use(middleware.Secure)  // 一些安全设置
	g.Use(mw...)
	g.NoRoute(func(c *gin.Context) {
		c.String(http.StatusNotFound, "The incorrect api route")
	})

	// health check handlers
	check := g.Group("/sd")
	{
		check.GET("/health", sd.HealthCheck)
		check.GET("/disk", sd.DiskCheck)
		check.GET("/cpu", sd.CPUCheck)
		check.GET("/ram", sd.RAMCheck)
	}

	u := g.Group("/v1/user")
	{
		u.POST("", user.Create)
	}

	return g
}
