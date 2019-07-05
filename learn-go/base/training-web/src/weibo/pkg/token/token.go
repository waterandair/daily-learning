package token

import (
	"log"
	"time"

	"github.com/dgrijalva/jwt-go"
	"github.com/labstack/echo"
	"github.com/spf13/viper"
)

// JWT Payload
type JwtContext struct {
	Id       uint64 `json:"id"`       // 用户id
	Username string `json:"username"` // 用户姓名
}

/* 生成 token */
func Sign(jwtContext JwtContext, secret string) (tokenString string, err error) {

	// 秘钥
	if secret == "" {
		secret = viper.GetString("jwt_secret")
	}

	// 指定签名算法和 JWT Payload
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, jwt.MapClaims{
		"id":       jwtContext.Id,
		"username": jwtContext.Username,
		"nbf":      time.Now().Unix(), // JWT Token 生效时间
		"iat":      time.Now().Unix(), // JWT Token 签发时间
	})

	// token 加密
	tokenString, err = token.SignedString([]byte(secret))

	return tokenString, err
}

/* 从请求中获取 token */
func ParseRequest(ctx echo.Context) (*JwtContext, error) {
	// token 字段名
	authHeader := viper.GetString("auth_header")

	// web 从 cookie 拿 token
	authorization, err := ctx.Cookie(authHeader)
	if err != nil {
		return &JwtContext{}, err
	}

	t := authorization.Value
	return Parse(t)
}

/* 解析token */
func Parse(tokenString string) (*JwtContext, error) {

	log.Println("token: " + tokenString)
	// 秘钥
	secret := viper.GetString("jwt_secret")
	ctx := &JwtContext{}

	// 解析 token
	token, err := jwt.Parse(tokenString, secretFunc(secret))

	if err != nil {
		log.Fatal(err.Error())
		return ctx, err
	} else if claims, ok := token.Claims.(jwt.MapClaims); ok && token.Valid {
		ctx.Id = uint64(claims["id"].(float64))
		ctx.Username = claims["username"].(string)
		return ctx, nil
	} else {
		log.Fatal("2" + err.Error())
		return ctx, err
	}
}

/* 检验加密算法 */
func secretFunc(secret string) jwt.Keyfunc {
	return func(token *jwt.Token) (interface{}, error) {
		if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
			return nil, jwt.ErrSignatureInvalid
		}
		return []byte(secret), nil
	}
}
