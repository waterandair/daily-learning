package main

import (
	"github.com/gin-gonic/gin"
	"apiserver/router"
	"log"
	"net/http"
	"time"
	"errors"
)

var (
	port = ":8080"
)

func main() {
	// 初始化 gin
	g := gin.New()
	// gin middlewares
	middlewares := []gin.HandlerFunc{}
	// 路由
	router.Load(g, middlewares...)

	// 检测健康状况
	go func() {
		if err := pingServer(); err != nil {
			log.Fatal("The router has no response, or it might took too long to start up.", err)
		}
		log.Print("The router has been deployed successfully.")
	}()
	// 启动
	log.Printf("Start to listening the incoming requests on http address: %s", ":8080")
	log.Printf(http.ListenAndServe(port, g).Error())
}

/*
心跳加测
	开启一个 goroutine 进行心跳检测
	每隔一秒请求一次服务器,如果有 10 次失败,就返回 error,并终止程序
*/
func pingServer() error {
	for i :=0; i < 10; i++ {
		resp, err := http.Get("http://127.0.0.1" + port + "/sd/health")
		if err == nil && resp.StatusCode == 200 {
			return nil
		}

		log.Print("Waiting for the router, retry in 1 second.")
		time.Sleep(time.Second)
	}

	return errors.New("server error")
}
