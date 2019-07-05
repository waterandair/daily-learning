package middleware

import (
	"github.com/labstack/echo"
	"github.com/spf13/viper"
	"net/http"
	"time"
	"weibo/controllers"
	"weibo/pkg/errno"
	"weibo/pkg/token"
	"weibo/services"
)

type Auth struct {
	us *services.UserService
}

func NewAuthMiddleWare(us *services.UserService) *Auth {
	return &Auth{
		us: us,
	}
}

/* 登录中间件 */
func (auth *Auth) AuthMiddleWare(next echo.HandlerFunc) echo.HandlerFunc {

	return func(c echo.Context) error {
		// 解析 token
		jwtPayload, err := token.ParseRequest(c)
		if err != nil {
			res := controllers.MakeResponse(errno.ErrToken, "请先登录")
			return c.JSON(http.StatusOK, res)
		}

		// 获取用户信息
		user, err := auth.us.FindById(jwtPayload.Id)
		if err != nil {
			cookie := new(http.Cookie)
			cookie.Name = viper.GetString("auth_header")
			cookie.Value = ""
			cookie.Expires = time.Now()
			c.SetCookie(cookie)

			res := controllers.MakeResponse(errno.ErrToken, "用户信息无效")
			return c.JSON(http.StatusOK, res)
		}
		// 解析 token 成功， 记录用户信息
		c.Set("user", user)
		return next(c)
	}

}
