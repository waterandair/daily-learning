package unit

import (
	"fmt"

	"github.com/jinzhu/gorm"
	_ "github.com/jinzhu/gorm/dialects/mysql"
	"github.com/spf13/viper"
)

/* 打开数据库 */
func NewMysqlConn() *gorm.DB {
	username := viper.GetString("db.username")
	password := viper.GetString("db.password")
	addr := viper.GetString("db.addr")
	name := viper.GetString("db.name")

	// 数据库连接 user:password@/dbname?charset=utf8&parseTime=True&loc=Local
	config := fmt.Sprintf("%s:%s@tcp(%s)/%s?charset=utf8&parseTime=%s&loc=%s",
		username,
		password,
		addr,
		name,
		"True",
		"Local")

	db, err := gorm.Open("mysql", config)
	if err != nil {
		panic(err)
	}

	//db.DB().SetMaxOpenConns(20000) // 用于设置最大打开的连接数，默认值为0表示不限制.设置最大的连接数，可以避免并发太高导致连接mysql出现too many connections的错误。
	db.DB().SetMaxIdleConns(0) // 用于设置闲置的连接数.设置闲置的连接数则当开启的一个连接使用完成后可以放在池里等候下一次使用。
	return db
}

/* 关闭数据库 */
func CloseMysqlConn(db *gorm.DB) {
	db.Close()
}
