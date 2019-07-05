package errno

/**
错误码说明：

	+------------- +----------------+---------------+
	|      1       |       00       |       02      |
	+--------------+----------------+---------------+
	|   错误级别    |   服务模块代码   |  具体错误代码   |
	+--------------+----------------+---------------+

	- 服务级别错误：
					1 为系统级错误
					2 为服务级错误，通常是由用户非法操作引起的

	- code = 0 说明是正确返回， code > 0 说明是错误返回
*/
var (
	// 系统级别错误
	OK                  = &Errno{Code: 0, Message: "OK"}
	InternalServerError = &Errno{Code: 10001, Message: "Internal server error."}
	ErrBind             = &Errno{Code: 10002, Message: "Error occurred while binding the request body to the struct."}
	ErrRedis            = &Errno{Code: 10003, Message: "Redis error"}

	// 服务级别错误
	ErrValidation        = &Errno{Code: 20001, Message: "Validation failed."}
	ErrDatabase          = &Errno{Code: 20002, Message: "Database error."}
	ErrToken             = &Errno{Code: 20003, Message: "Error occurred while signing the JSON web token."}
	ErrDuplicateFollow   = &Errno{Code: 20004, Message: "Duplicate Follow."}
	ErrPage              = &Errno{Code: 20005, Message: "Wrong page request."}
	ErrUserNameExisted   = &Errno{Code: 20006, Message: "Username is existed"}
	ErrEmailExisted      = &Errno{Code: 20007, Message: "Email is existed"}
	ErrNotEmail          = &Errno{Code: 20008, Message: "The email format is incorrect"}
	ErrUserNotFound      = &Errno{Code: 20102, Message: "The user was not found."}
	ErrEncrypt           = &Errno{Code: 20101, Message: "Error occurred while encrypting the user password."}
	ErrTokenInvalid      = &Errno{Code: 20103, Message: "The token was invalid."}
	ErrPasswordIncorrect = &Errno{Code: 20104, Message: "The password was incorrect."}
)
