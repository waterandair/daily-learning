package database

import (
	"database/sql"
	_ "github.com/go-sql-driver/mysql"
	"log"
)

var SqlDB *sql.DB

func init() {
	var err error
	SqlDB, err = sql.Open("mysql", "root:000000@/test?charset=utf8")
	if err != nil {
		log.Fatalln(err.Error())
	}
	SqlDB.SetMaxIdleConns(20)  //设置数据库的连接池最大空闲连接
	SqlDB.SetMaxOpenConns(20)  //设置数据库的最大数据库连接
	err = SqlDB.Ping()
	if err != nil {
		log.Fatalln(err.Error())
	}
}

/*
CREATE TABLE `person` (
`id` int(11) NOT NULL AUTO_INCREMENT,
`first_name` varchar(40) NOT NULL DEFAULT '',
`last_name` varchar(40) NOT NULL DEFAULT '',
PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
*/