package controllers

import (
	"github.com/spf13/viper"
	"net/http"
	"strconv"
	"time"
	"weibo/pkg/errno"
	"weibo/pkg/token"

	"weibo"

	"github.com/labstack/echo"
)

// 微博模块控制器
type PostController struct {
	ps weibo.PostService
	us weibo.UserService
	ls weibo.LikeService
	fs weibo.FollowService
}

// 微博列表响应
type ListResponse struct {
	UserId        uint64            `json:"user_id"`
	UserName      string            `json:"user_name"`
	Posts         []weibo.Post      `json:"posts"`
	IsLogin       bool              `json:"is_login"`
	PostsCount    uint64            `json:"posts_count"`
	FollowsCount  uint64            `json:"follows_count"`
	FansCount     uint64            `json:"fans_count"`
	MessagesCount uint64            `json:"messages_count"`
	LikesCounts   map[uint64]uint64 `json:"likes_counts"`
	CurrentPage   uint64            `json:"page"`
	PageCount     uint64            `json:"page_all"`
}

/* 创建控制器 */
func NewPostController(ps weibo.PostService, us weibo.UserService, ls weibo.LikeService, fs weibo.FollowService) *PostController {
	return &PostController{
		ps: ps,
		us: us,
		ls: ls,
		fs: fs,
	}
}

/* 首页-微博列表 */
func (c *PostController) List(ctx echo.Context) error {
	// 页码
	page := ctx.QueryParam("page")
	if page == "" {
		page = "1"
	}
	pageId, err := strconv.ParseUint(page, 10, 64)
	if err != nil {
		return ctx.String(http.StatusOK, err.Error())
	}

	// 页 size
	limit := viper.GetInt("default_limit")
	offset := uint64(limit) * (pageId - 1)

	// 微博总数
	postsAllCount := c.ps.CountAll()
	// 总页数
	pageCount := postsAllCount / uint64(limit)
	if postsAllCount%uint64(limit) != 0 || pageCount == 0 {
		pageCount ++
	}

	// 判断当前页码是否规范
	if pageId < 1 || pageId > pageCount {
		response := MakeResponse(errno.ErrPage, "请输入正确页码")
		return ctx.JSON(http.StatusOK, response)
	}

	// 微博列表
	posts, err := c.ps.List(offset, uint64(limit))
	if err != nil {
		return ctx.String(http.StatusOK, err.Error())
	}

	// 点赞数
	likesCounts := make(map[uint64]uint64)
	for _, post := range posts {
		likesCounts[post.ID], err = c.ls.GetLikesCount(post.ID)
		if err != nil {
			failOnError(err, "GetLikesCount error")
		}
	}

	// 响应 data
	var data = &ListResponse{
		CurrentPage: pageId,
		PageCount:   pageCount,
		IsLogin:     false,
		Posts:       posts,
		LikesCounts: likesCounts,
	}

	// 判断是否已登录 根据 cookie 中的 Authorization 关键字
	jwt, err := token.ParseRequest(ctx)
	userId := uint64(0)
	if err == nil {
		// 登录状态设置 user
		user, err := c.us.FindById(jwt.Id)
		if err != nil {
			cookie := new(http.Cookie)
			cookie.Name = viper.GetString("auth_header")
			cookie.Value = ""
			cookie.Expires = time.Now()
			ctx.SetCookie(cookie)
			res := MakeResponse(errno.ErrToken, "用户信息无效")
			return ctx.JSON(http.StatusOK, res)
		}

		ctx.Set("user", user)

		userId = user.ID
		data.UserId = user.ID
		data.UserName = user.Name
	}

	// 登录状态 获取微博数、关注数、粉丝数、消息数
	if userId != 0 {
		// 微博数
		postsCount, err := c.ps.GetPostsCountByUserId(userId)
		failOnError(err, "GetPostsCount error")

		// 关注数
		followsCount, err := c.fs.GetFollowCount(userId)
		failOnError(err, "GetFollowsCount error")

		// 粉丝数
		fansCount, err := c.fs.GetFansCount(userId)
		failOnError(err, "GetFansCount error")

		// 消息数
		messagesCount, err := c.ls.GetMessagesCount(userId)
		failOnError(err, "GetMessagesCount error")

		data.PostsCount = postsCount
		data.FollowsCount = followsCount
		data.FansCount = fansCount
		data.MessagesCount = messagesCount

		data.IsLogin = true
	}

	return ctx.Render(http.StatusOK, "index.html", data)
}

/* 写微博 get 请求 */
func (c *PostController) CreateForm(ctx echo.Context) error {
	user := ctx.Get("user").(*weibo.User)
	userName := user.Name
	return ctx.Render(http.StatusOK, "create_post.html", userName)
}

/* 写微博 post 请求 */
func (c *PostController) Create(ctx echo.Context) error {
	user := ctx.Get("user").(*weibo.User)
	content := ctx.FormValue("content")

	post := weibo.Post{
		UserId:   user.ID,
		UserName: user.Name,
		Content:  content,
	}

	// 添加数据库 posts 表记录, 增加 redis 记录数
	if err := c.ps.Create(&post); err != nil {
		return ctx.String(http.StatusOK, err.Error())
	}


	return ctx.Redirect(302, "/v1/")
}
