package errno

import "fmt"

type Errno struct {
	Code    int
	Message string
}

func (err Errno) Error() string {
	return err.Message
}

type Err struct {
	*Errno
	Err error
}

func (err *Err) Error() string {
	return fmt.Sprintf("Err - code: %d, message: %s, error: %s", err.Code, err.Message, err.Err)
}

// 给自定义错误添加额外的信息
func (err *Err) Add(message string) error {
	err.Message += " " + message
	return err
}

// 给自定义错误添加额外格式化的信息
func (err *Err) Addf(format string, args ...interface{}) error {
	err.Message += " " + fmt.Sprintf(format, args...)
	return err
}

// 新建自定义错误
func New(errno *Errno, err error) *Err {
	return &Err{
		Errno: errno,
		Err:   err,
	}
}

// 解析自定义错误
func DecodeErr(err error) (int, string) {
	if err == nil {
		return OK.Code, OK.Message
	}

	switch typed := err.(type) {
	case *Err:
		return typed.Code, typed.Message
	case *Errno:
		return typed.Code, typed.Message
	default:

	}

	return InternalServerError.Code, err.Error()
}

func IsErrUserNotFound(err error) bool {
	code, _ := DecodeErr(err)
	return code == ErrUserNotFound.Code
}
