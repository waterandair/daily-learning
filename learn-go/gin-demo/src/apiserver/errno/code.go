package errno
/**
错误码说明
	+------------- +----------------+---------------+
	|      1       |       00       |       02      |
	+--------------+----------------+---------------+
	|   错误级别    |   服务模块代码   |  具体错误代码   |
	+--------------+----------------+---------------+

	- 服务级别错误：1 为系统级错误；2 为服务级错误，通常是由用户非法操作引起的
	- code = 0 说明是正确返回，code > 0 说明是错误返回
 */
var (
	// common errors
	OK                  = &Errno{Code: 0, Message: "OK"}
	InternalServerError = &Errno{Code: 10001, Message: "Internal server error."}
	ErrBind             = &Errno{Code: 10002, Message: "Error occurred while binding the request body to the struct."}

	// user errors
	ErrUserNotFound = &Errno{Code: 20102, Message: "The user was not found."}
)