package main

import (
	"github.com/astaxie/beego/orm"
	_ "github.com/go-sql-driver/mysql"
	"fmt"
)

type User2 struct {
	Uid int `orm:"pk"`
	Name string
}

func init() {
	// 注册驱动
	orm.RegisterDriver("mysql", orm.DRMySQL)
	// 设置默认数据库
	orm.RegisterDataBase("default", "mysql", "root:000000@/test?charset=utf8", 30)
	// 注册定义 model
	orm.RegisterModel(new(User2))
	// 创建table
	orm.RunSyncdb("default", false, true)

	// 根据数据库的别名，设置数据库的连接池最大空闲连接, 与 RegisterDataBase 中的第4个 参数同样含义
	orm.SetMaxIdleConns("default", 30)
	// 根据数据库的别名，设置数据库的最大数据库连接 (go >= 1.2) 与 RegisterDataBase 中的第5个 参数同样含义
	orm.SetMaxOpenConns("default", 30)
	// 打印调试
	// orm.Debug = true
}

func main() {
	o := orm.NewOrm()

	user := User2{Name:"zj"}

	// 插入表
	id, err := o.Insert(&user)
	fmt.Printf("ID: %d, ERR: %v \n", id, err)

	// 更新表
	user.Name = "zj2"
	num, err := o.Update(&user)
	fmt.Printf("num: %d, err: %v \n", num, err)

	// 读取 one
	u := User2{Uid: user.Uid}
	err = o.Read(&u)
	fmt.Printf("err: %v \n", err)
	fmt.Printf("name: %v \n", u.Name)

	// 删除表
	//num, err = o.Delete(&u)
	//fmt.Printf("num: %d, err: %v \n", num, err)

}


