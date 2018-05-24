package model

import (
	"time"
)

type Userinfo struct {
	Uid int `orm:"pk"`  // 如果表的主键不是id, 那么需要加上pk注释, 显式的说这个字段是主键
	Name string
	Departname string
	Created time.Time
}

type User struct {
	Uid int `orm:"default(0);pk;auto"`
	Uid2 int `orm:"default(0)"`
	Name string
	Departname  string `orm:"default(研发部)"`
	Created time.Time `orm:"auto_now_add;default(time.Now())"`
	Profile *Profile `orm:"null;rel(one);"`  // 一对一关系
	Posts []*Post `orm:"reverse(many)"`  // 一对多的反向关系
}

type Profile struct {
	Id int `orm:"pk"`
	Age int16
	User *User `orm:"reverse(one)"`  // 一对一反向关系(可选)
}

type Post struct {
	Id int
	Title string
	User *User `orm:"rel(fk)"`  // 一对多关系
	Tags []*Tag `orm:"rel(m2m)"`  // 多对多关系
}

type Tag struct {
	Id int
	Name string
	Posts []*Post `orm:"reverse(many)"`
}
