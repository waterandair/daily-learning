package main

import (
	"github.com/gin-gonic/gin"
	"net/http"
	"time"
	"log"
)

func initRouter() *gin.Engine {
	router := gin.Default()

	// : catch-one
	router.GET("/user/:name", func(c *gin.Context) {
		name := c.Param("name")
		c.String(http.StatusOK, "hello %s", name)
	})

	// * catch-all , 只能放在最后面
	router.GET("/user/:name/*action", func(c *gin.Context) {
		name := c.Param("name")
		name2 := c.Param("name2")
		action := c.Param("action")
		message := name + " is " + action + " - " + name2
		c.String(http.StatusOK, message)
	})

	// query string
	router.GET("query-string", func(c *gin.Context) {
		a := c.DefaultQuery("a", "default-a")
		b := c.Query("b")
		c.String(http.StatusOK, "a: %s, b: %s", a, b)
	})

	// body
	// curl -X POST http://127.0.0.1:8000/body/params?c="ccc" -d "a=aaa&b=a"
	// curl -X POST http://127.0.0.1:8000/body/params?c="ccc" -H "Content-Type: application/json" -d '{"name": "zj", "age":25}'
	router.POST("body/:params", QueryBody)

	// file
	// curl -X POST http://127.0.0.1:8000/file -F "upload=@/home/zj/Pictures/1.png" -H "Content-Type: multipart/form-data"
	router.POST("/file", UploadFile)

	// files
	// curl -X POST http://127.0.0.1:8000/files -F "uploads=@/home/zj/Pictures/1.png" -F "uploads=@/home/zj/Pictures/2.jpg" -H "Content-Type: multipart/form-data"
	router.POST("/files", UploadFiles)

	// 表单上传
	router.LoadHTMLGlob("templates/*")
	router.GET("/upload", func(c *gin.Context) {
		c.HTML(http.StatusOK, "upload.html", gin.H{
			"Name": "文件上传",
		})
	})

	// 重定向
	router.GET("/redirect", func(c *gin.Context) {
		c.Redirect(http.StatusMovedPermanently, "https://www.github.com/waterandair")
	})

	// 分组路由
	v1 := router.Group("/v1")
	v1.GET("/login", func(c *gin.Context) {
		c.String(http.StatusOK, "v1 login")
	})
	v2 := router.Group("/v2")
	v2.GET("/login", func(c *gin.Context) {
		c.String(http.StatusOK, "v2 login")
	})

	// 单个路由中间件
	// curl http://127.0.0.1:8000/before
	router.GET("/before", MiddleWare(), func(c *gin.Context) {
		request := c.MustGet("request").(string)
		c.JSON(http.StatusOK, gin.H{
			"middleware_request": request,
		})
	})

	// 群组中间件
	group1 := router.Group("/group1", MiddleWare())
	group1.GET("middleware", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{
			"msg": "群组中间件",
		})
	})
	// or
	group2 := router.Group("group2")
	group2.Use(MiddleWare())
	{
		group2.GET("middleware", func(c *gin.Context) {
			c.JSON(http.StatusOK, gin.H{
				"msg": "群组中间件",
			})
		})
	}

	// 全局中间件
	// 主能让 router.Use(MiddleWare()) 之后的路由生效
	// curl http://127.0.0.1:8000/middleware
	router.Use(MiddleWare())
	{
		router.GET("/middleware", func(c *gin.Context) {
			request := c.MustGet("request").(string)
			req, _ := c.Get("request")
			c.JSON(http.StatusOK, gin.H{
				"middle_request": request,
				"request": req,
			})
		})
	}

	// 协程
	router.GET("sync", func(c *gin.Context) {
		time.Sleep(5 * time.Second)
		log.Println("Done in path" + c.Request.URL.Path)
	})

	router.GET("/async", func(c *gin.Context) {
		cCp := c.Copy()
		go func() {
			time.Sleep(5 * time.Second)
			log.Println("Done! in path" + cCp.Request.URL.Path)
		}()
	})

	return router
}
