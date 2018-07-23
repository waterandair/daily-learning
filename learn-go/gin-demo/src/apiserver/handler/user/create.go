package user

import (
	"github.com/gin-gonic/gin"
	"net/http"
	"apiserver/errno"
	"github.com/lexkong/log"
	"fmt"
)

func Create(c *gin.Context) {
	var r struct{
		Username string `json:"username"`
		Password string `json:"password"`
	}

	var err error

	if err = c.Bind(&r); err != nil {
		c.JSON(http.StatusOK, errno.ErrBind)
		return
	}

	log.Debugf("username is: [%s], password is [%s]", r.Username, r.Password)
	if r.Username == "" {
		err = errno.New(errno.ErrUserNotFound, fmt.Errorf("username can not found in db: xxxxx")).Add("this is add message")
		log.Errorf(err, "get and error")
	}

	if errno.IsErrUserNotFound(err) {
		log.Debug("err type is ErrUserNotFound ")
	}

	if r.Password == "" {
		err = fmt.Errorf("password is empty")
	}

	code, message := errno.DecodeErr(err)
	c.JSON(http.StatusOK, gin.H{"code": code, "message": message})
}
