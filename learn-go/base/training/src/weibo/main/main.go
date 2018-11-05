package main

import (
	"html/template"
	"io"
	"log"

	"weibo/controllers"
	"weibo/middleware"
	"weibo/services"
	"weibo/unit"

	"github.com/labstack/echo"
	"github.com/spf13/viper"
)

func main() {

	e := echo.New()

	/**
	初始化配置文件
	 */
	if err := unit.InitConfig(""); err != nil {
		panic(err)
	}

	/**
	初始化数据库连接
	 */
	var db = unit.NewMysqlConn()
	defer db.Close()

	/**
	初始化 redis 连接
	*/
	var redis = unit.NewRedisConn()
	defer redis.Close()

	/**
	初始化 grpc 客户端
	*/
	grpcLike := unit.NewGrpcLikeConn()
	defer grpcLike.GrpcConn.Close()

	/**
	初始化 rabbitMq like 客户端
	 */
	var rabbitMq = unit.NewRabbitMqConn("like")
	defer rabbitMq.Conn.Close()
	defer rabbitMq.Channel.Close()

	/**
	初始化 service
	*/
	us := services.NewUserService(db)
	ps := services.NewPostService(db, redis)
	fs := services.NewFollowService(db, redis)
	ls := services.NewLikeService(db, redis, grpcLike.GrpcClient, rabbitMq)

	/**
	初始化控制器
	*/

	// 用户模块
	uc := controllers.NewUserController(us)
	// 博文模块
	pc := controllers.NewPostController(ps, us, ls, fs)
	// 关注模块
	fc := controllers.NewFollowController(fs)
	// 点赞模块
	lc := controllers.NewLikeController(ls)

	/**
	消费 点赞模块 消息队列
	*/
	go lc.ConsumeMessage()

	/**
	初始化模板
	*/
	t := &Template{
		templates: template.Must(template.ParseGlob("../views/*.html")),
	}
	e.Renderer = t

	/**
	注册路由
	*/

	// api 版本
	version := viper.GetString("version")

	authMiddleWare := middleware.NewAuthMiddleWare(us)

	// 博文模块
	e.GET("/"+version+"/", pc.List).Name = "index"
	e.GET("/"+version+"/post/create", pc.CreateForm, authMiddleWare.AuthMiddleWare)
	e.POST("/"+version+"/post/create", pc.Create, authMiddleWare.AuthMiddleWare)
	e.GET("/"+version+"/post/create", pc.CreateForm, authMiddleWare.AuthMiddleWare)
	e.POST("/"+version+"/post/create", pc.Create, authMiddleWare.AuthMiddleWare)

	// 用户模块
	e.GET("/"+version+"/register", uc.LogoutForm)
	e.POST("/"+version+"/register", uc.Register)
	e.GET("/"+version+"/login", uc.LoginForm)
	e.POST("/"+version+"/login", uc.Login)

	// 关注模块
	e.POST("/"+version+"/follow", fc.Follow, authMiddleWare.AuthMiddleWare)

	// 点赞
	e.POST("/"+version+"/like", lc.Like, authMiddleWare.AuthMiddleWare)
	// 消息
	e.GET("/"+version+"/like/:nums", lc.Message, authMiddleWare.AuthMiddleWare)

	/**
	注册静态文件
	*/
	e.Static("/static", "../assets")

	log.Fatal(e.Start("0.0.0.0:8000"))
}

// 模板
type Template struct {
	templates *template.Template
}

/* 渲染模板 */
func (t *Template) Render(w io.Writer, name string, data interface{}, c echo.Context) error {
	return t.templates.ExecuteTemplate(w, name, data)
}

