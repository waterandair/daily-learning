package main

import (
	"github.com/gin-gonic/gin"
	"apiserver/router"
	"apiserver/config"
	"github.com/lexkong/log"
	"net/http"
	"time"
	"errors"
	"github.com/spf13/viper"
	"github.com/spf13/pflag"
	"apiserver/model"
)

var (
	cfg = pflag.StringP("config", "c", "", "apiserver config file path")  // 命令行参数
)

func main() {
	pflag.Parse()

	// 初始化配置
	if err := config.Init(*cfg); err != nil {
		panic(err)
	}

	// 设置 gin 模式
	gin.SetMode(viper.GetString("runmode"))

	// 初始化 gin
	g := gin.New()

	// gin middlewares
	middlewares := []gin.HandlerFunc{}

	// 路由
	router.Load(g, middlewares...)

	// 初始化数据库
	model.DB.Init()
	defer model.DB.Close()

	// 检测健康状况
	go func() {
		if err := pingServer(); err != nil {
			log.Fatal("The router has no response, or it might took too long to start up.", err)
		}
		log.Info("The router has been deployed successfully.")
	}()

	// 启动
	log.Infof("Start to listening the incoming requests on http address: %s", viper.GetString("addr"))
	log.Info(http.ListenAndServe(viper.GetString("addr"), g).Error())
}

/*
心跳加测
	开启一个 goroutine 进行心跳检测
	每隔一秒请求一次服务器,如果有 10 次失败,就返回 error,并终止程序
*/
func pingServer() error {
	for i :=0; i < viper.GetInt("max_ping_count"); i++ {
		resp, err := http.Get(viper.GetString("url") + "/sd/health")
		if err == nil && resp.StatusCode == 200 {
			return nil
		}

		log.Info("Waiting for the router, retry in 1 second.")
		time.Sleep(time.Second)
	}

	return errors.New("server error")
}
