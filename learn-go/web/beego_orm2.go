package main

import (
	"github.com/astaxie/beego/orm"
	_ "github.com/go-sql-driver/mysql"
	"model"
	"fmt"
)

func init() {
	// 注册驱动
	orm.RegisterDriver("mysql", orm.DRMySQL)
	// 设置默认数据库
	orm.RegisterDataBase("default", "mysql", "root:000000@/test?charset=utf8", 30)
	// 注册定义 model
	orm.RegisterModel(new(model.User), new(model.Post), new(model.Profile), new(model.Tag))
	// 创建table
	orm.RunSyncdb("default", false, true)

	// 根据数据库的别名，设置数据库的最大空闲连接, 与 RegisterDataBase 中的第4个 参数同样含义
	orm.SetMaxIdleConns("default", 30)
	// 根据数据库的别名，设置数据库的最大数据库连接 (go >= 1.2) 与 RegisterDataBase 中的第5个 参数同样含义
	orm.SetMaxOpenConns("default", 30)
	// 打印调试
	// orm.Debug = true
}

func main() {
	o := orm.NewOrm()
	// 插入数据
	user := model.User{Name: "zj11"}
	users := []model.User{
		{Name: "multi_zj1", Departname:"研发部"},
		{Name: "multi_zj2", Departname:"研收部"},
		{Name: "multi_zj3", Departname:"研发部"},
	}

	// 插入一条
	InsertOne(o, user)
	// 插入多条
	InsertMulti(o, users)

	//user := model.User{Uid: 1}
	//UpdateOne(o, &user)
	//updateMulti(o, &user)

	// 查询
	//user := model.User{Uid: 1}
	//SelectOne(o, &user)
	//Filter(o)

	// 原生 sql
	// Sql(o)

}

func InsertOne(o orm.Ormer, user model.User) {
	fmt.Println("##########")
	id, err := o.Insert(&user)
	if err == nil {
		fmt.Println("id: ", id)
	} else {
		println(err.Error())
	}

	fmt.Println("##########")
}

func InsertMulti(o orm.Ormer, users []model.User) {
	// bulk 为 1 的时候, 按照 slice 中的顺序插入
	nums, err := o.InsertMulti(100, users)
	if err == nil {
		fmt.Println("insert nums:", nums)
	}
}

func UpdateOne(o orm.Ormer, user *model.User)  {
	if o.Read(user) == nil {
		user.Name = "update_name"
		if num, err := o.Update(user); err == nil{
			fmt.Println("num", num)
		}
	}
}

func updateMulti(o orm.Ormer, user *model.User) {
	user.Name = "name"
	user.Departname = "验收部"
	o.Update(user, "Name", "Departname")
}

func SelectOne(o orm.Ormer, user *model.User) {
	err := o.Read(user)
	if err == orm.ErrNoRows {
		fmt.Println("查询不到")
	} else if err == orm.ErrMissPK {
		fmt.Println("找不到主键")
	} else {
		fmt.Println(user.Uid, user.Name)
	}
}

func Filter(o orm.Ormer) {
	var user model.User
	var users []*model.User
	var maps []orm.Params
	qs := o.QueryTable(user)
	qs.Filter("Uid__gt", 2).Values(&maps)  // id大于1

	for _, row := range users {
		fmt.Println(row)
	}

	for _, m := range maps {
		fmt.Println(m["Uid"])
	}

}


func Sql(o orm.Ormer) {
	//var r orm.RawSeter
	var users []*model.User
	sql := o.Raw("select * from user")
	//fmt.Println(sql)
	sql.QueryRows(&users)
	println(users[0].Name)

	sql2 := o.Raw("insert into user (name, departname) values (?, ?)", "sql", "sql")
	qs, err := sql2.Exec()
	if err == nil {
		nums, _ := qs.RowsAffected()
		id, _ := qs.LastInsertId()
		println(nums, id)
	} else {
		fmt.Println(err)
	}


}



