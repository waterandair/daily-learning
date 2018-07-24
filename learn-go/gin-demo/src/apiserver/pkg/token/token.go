package token

import (
	"errors"
	"fmt"
	"github.com/dgrijalva/jwt-go"
	"github.com/gin-gonic/gin"
	"github.com/spf13/viper"
	"time"
)

var (
	// 请求中灭有
	ErrMissingHeader = errors.New("the length of `Authorization` is zero ")
)

// jwt
type JwtContext struct {
	Id       uint64
	Username string
}

// 生成 token
func Sign(c *gin.Context, jwtContext JwtContext, secret string) (tokenstring string, err error) {
	if secret == "" {
		secret = viper.GetString("jwt_secret")
	}

	// 生成 token
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, jwt.MapClaims{
		"id":       jwtContext.Id,
		"username": jwtContext.Username,
		"nbf":      time.Now().Unix(),
		"iat":      time.Now().Unix(),
	})

	// 给 token 加密
	tokenstring, err = token.SignedString([]byte(secret))
	return
}

// 解析 token
func ParseRequest(c *gin.Context) (*JwtContext, error) {
	header := c.Request.Header.Get("Authorization")

	secret := viper.GetString("jwt_secret")

	if len(header) == 0 {
		return &JwtContext{}, ErrMissingHeader
	}

	var t string

	fmt.Sscanf(header, "Bearer %s", &t)
	return Parse(t, secret)
}

func Parse(tokenString, secret string) (*JwtContext, error) {
	ctx := &JwtContext{}

	// 解析 token
	token, err := jwt.Parse(tokenString, secretFunc(secret))

	if err != nil {
		return ctx, err
	} else if claims, ok := token.Claims.(jwt.MapClaims); ok && token.Valid {
		ctx.Id = uint64(claims["id"].(float64))
		ctx.Username = claims["username"].(string)
		return ctx, nil
	} else {
		return ctx, err
	}
}

// 检验格式
func secretFunc(secret string) jwt.Keyfunc {
	return func(token *jwt.Token) (interface{}, error) {
		if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
			return nil, jwt.ErrSignatureInvalid
		}
		return []byte(secret), nil
	}
}
