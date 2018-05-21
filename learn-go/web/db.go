package main

import (
	"database/sql"
	"fmt"
	_ "github.com/go-sql-driver/mysql"
)

func checkErr(err error) {
	if err != nil {
		panic(err)
	}

}

func main() {
	db, err := sql.Open("mysql", "root:000000@/test?charset=utf8")
	checkErr(err)

	stmt, err := db.Prepare("insert into userinfo (username, department, created) values (?, ?, ?)")
	checkErr(err)

	res, err := stmt.Exec("zj", "研发部", "2017-01-03")
	checkErr(err)

	id, err := res.LastInsertId()
	checkErr(err)

	fmt.Println(id)

	// 更新数据
	stmt, err = db.Prepare("update userinfo set username=? where uid=?")
	checkErr(err)

	res, err = stmt.Exec("张吉", id)
	checkErr(err)

	affect, err := res.RowsAffected()
	checkErr(err)

	fmt.Println(affect)

	// 查询数据
	rows, err := db.Query("select * from userinfo")
	checkErr(err)

	for rows.Next() {
		var uid int
		var username string
		var department string
		var created string
		err = rows.Scan(&uid, &username, &department, &created)
		checkErr(err)

		fmt.Println(uid, username, department, created)
	}

	stmt, err = db.Prepare("select * from userinfo where uid=?")
	rows, err = stmt.Query(1)
	for rows.Next() {
		var uid int
		var username string
		var department string
		var created string
		err = rows.Scan(&uid, &username, &department, &created)
		checkErr(err)

		fmt.Println(uid, username, department, created)
	}



}
