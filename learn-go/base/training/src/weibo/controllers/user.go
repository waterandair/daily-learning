package controllers

import (
	"github.com/spf13/viper"
	"net/http"
	"regexp"
	"time"
	"weibo"
	"weibo/pkg/auth"
	"weibo/pkg/errno"
	"weibo/pkg/token"

	"github.com/go-sql-driver/mysql"
	"github.com/labstack/echo"
)

// 用户模块控制器
type UserController struct {
	us weibo.UserService
}

// 注册请求结构体
type RegisterRequest struct {
	Username string `json:"username"`
	Password string `json:"password"`
	Email    string `json:"email"`
}

// 登录请求结构体
type LoginRequest struct {
	Username string `json:"username"`
	Password string `json:"password"`
}

// 登录响应构体
type LoginResponse struct {
	Token string `json:"token"`
}

/* 新建控制器 */
func NewUserController(us weibo.UserService) *UserController {
	return &UserController{
		us: us,
	}
}

/* 注册 get 请求 */
func (c *UserController) LogoutForm(ctx echo.Context) error {
	return ctx.Render(http.StatusOK, "register.html", nil)
}

/* 注册 post 请求 */
func (c *UserController) Register(ctx echo.Context) error {
	var r RegisterRequest
	if err := ctx.Bind(&r); err != nil {
		return ctx.String(http.StatusOK, err.Error())
	}

	// 验证用户名
	if r.Username == "" {
		return ctx.JSON(http.StatusOK, MakeResponse(errno.New(errno.ErrValidation, nil).Add("Username is empty."), "用户名格式错误"))
	}

	// 验证邮箱
	if m, _ := regexp.MatchString(`^([\w\.\_]{2,10})@(\w{1,}).([a-z]{2,4})$`, r.Email); !m {
		return ctx.JSON(http.StatusOK, MakeResponse(errno.New(errno.ErrNotEmail, nil), "邮箱格式错误"))
	}

	// 验证密码
	if r.Password == "" {
		return ctx.JSON(http.StatusOK, MakeResponse(errno.New(errno.ErrValidation, nil).Add("Password is empty."), "密码格式错误"))
	}

	u := weibo.User{
		Name:     r.Username,
		Password: r.Password,
		Email:    r.Email,
	}

	// 判断用户名是否已存在
	if _, err := c.us.FindByName(u.Name); err == nil {
		response := MakeResponse(errno.New(errno.ErrUserNameExisted, err), "用户名已存在")
		return ctx.JSON(http.StatusOK, response)
	}

	// 判断 email 是否已存在

	if _, err := c.us.FindByEmail(u.Email); err == nil {
		response := MakeResponse(errno.New(errno.ErrEmailExisted, err), "邮箱地址已被注册")
		return ctx.JSON(http.StatusOK, response)
	}

	// 加密密码
	if err := c.us.Encrypt(&u); err != nil {
		response := MakeResponse(errno.New(errno.ErrEncrypt, err), "密码加密失败")
		return ctx.JSON(http.StatusOK, response)
	}

	// 添加数据库 users 表记录
	if err := c.us.Create(&u); err != nil {
		mysqlErr, ok := err.(*mysql.MySQLError)
		if ok {
			if mysqlErr.Number == 1062 {
				response := MakeResponse(errno.New(errno.ErrDatabase, err), "用户名重复")
				return ctx.JSON(http.StatusOK, response)
			}
		}
		response := MakeResponse(errno.New(errno.ErrDatabase, err), "添加记录失败")
		return ctx.JSON(http.StatusOK, response)
	}

	response := MakeResponse(nil, nil)
	return ctx.JSON(http.StatusOK, response)
}

/* 登录 get 请求 */
func (c *UserController) LoginForm(ctx echo.Context) error {
	return ctx.Render(http.StatusOK, "login.html", nil)
}

/* 登录 post 请求 */
func (c *UserController) Login(ctx echo.Context) error {
	var r LoginRequest
	if err := ctx.Bind(&r); err != nil {
		return ctx.String(http.StatusOK, err.Error())
	}

	// 检查用户名
	if r.Username == "" {
		return ctx.JSON(http.StatusOK, MakeResponse(errno.New(errno.ErrValidation, nil).Add("Username is empty."), "用户名格式错误"))
	}

	// 检查密码
	if r.Password == "" {
		return ctx.JSON(http.StatusOK, MakeResponse(errno.New(errno.ErrValidation, nil).Add("Password is empty."), "密码格式错误"))
	}

	u := weibo.User{
		Name:     r.Username,
		Password: r.Password}

	// 获取用户信息
	user, err := c.us.FindByName(u.Name)
	if err != nil {
		return ctx.String(http.StatusOK, err.Error())
	}

	// 验证密码是否正确
	if err := auth.Compare(user.Password, u.Password); err != nil {
		return ctx.String(http.StatusOK, err.Error())
	}

	// 构造 token
	tokenStr, err := token.Sign(token.JwtContext{Id: user.ID, Username: user.Name}, "")
	if err != nil {
		return ctx.String(http.StatusOK, err.Error())
	}

	// 登录成功， 设置 cookie token
	cookie := new(http.Cookie)
	cookie.Name = viper.GetString("auth_header")
	cookie.Value = tokenStr
	cookie.Expires = time.Now().Add(time.Hour*365)
	cookie.Path = "/"
	ctx.SetCookie(cookie)
	ctx.Response().Header().Set("P3P:CP","NOI ADM DEV PSAi COM NAV OUR OTRo STP IND DEM")
	response := MakeResponse(nil, LoginResponse{Token:tokenStr})

	return ctx.JSON(http.StatusOK, response)
}
