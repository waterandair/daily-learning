package main

import (
	"os"
	"html/template"
	"fmt"
	"strings"
)

type Person struct {
	UserName string
	email string
}

type Person2 struct {
	UserName string
	Emails []string
	Friends []*Friend
}

type Friend struct {
	Fname string
}

func main() {
	//demo()
	//demo2()
	// 循环
	//demo3()
	// 条件
	//demo4()

	// 管道
	//pipelines()

	// 局部变量
	// Demo5()

	// 模板函数
	//demo6()

	//嵌套模板
	demo7()
}

func demo() {
	t := template.New("fieldname example")
	t, _ = t.Parse("hello {{.UserName}}!\n")
	p := Person{
		UserName: "zj",
	}
	t.Execute(os.Stdout, p)
}

// 小写开头的字段不会被解析
func demo2() {
	t := template.New("fieldname example")
	t, _ = t.Parse("hello {{.UserName}}!{{.email}} \n")
	p := Person{
		UserName: "zj",
		email: "123@qq.com",
	}
	t.Execute(os.Stdout, p)
}

func demo3() {
	f1 := Friend{Fname: "kobe"}
	f2 := Friend{Fname: "wade"}
	t := template.New("fieldname example")
	t, _ = t.Parse(`hello {{.UserName}}!
			{{range .Emails}}
				an email {{.}}
			{{end}}
			{{with .Friends}}
			{{range .}}
				my friend name is {{.Fname}}
			{{end}}
			{{end}}
			`)
	p := Person2{UserName: "zj",
		Emails:  []string{"1@qq.com", "2@qq.com"},
		Friends: []*Friend{&f1, &f2}}

	t.Execute(os.Stdout, p)
}

func demo4()  {
	// if 里面只能是 bool 值
	tEmpty := template.New("template test")
	tEmpty = template.Must(tEmpty.Parse("空 pipeline if demo: {{if ``}} 不会输出. {{end}}\n"))
	tEmpty.Execute(os.Stdout, nil)

	tWithValue := template.New("template test")
	tWithValue = template.Must(tWithValue.Parse("不为空的 pipeline if demo: {{if `anything`}} 我有内容，我会输出. {{end}}\n"))
	tWithValue.Execute(os.Stdout, nil)

	tIfElse := template.New("template test")
	tIfElse = template.Must(tIfElse.Parse("if-else demo: {{if `anything`}} if部分 {{else}} else部分.{{end}}\n"))
	tIfElse.Execute(os.Stdout, nil)
}

func pipelines() {
	t := template.New("template")
	t.Parse("hello {{.UserName | html}}!\n")
	p := Person2{
		UserName: "<h1>zj</h1>",
	}
	t.Execute(os.Stdout, p)
}

func Demo5() {
	t := template.New("test")
	t.Parse(`
		{{with $x := "output" | printf "%q"}}{{$x}}{{end}}
		{{with $x := "output"}}{{printf "%q" $x}}{{end}}
		{{with $x := "output"}}{{$x | printf "%q"}}{{end}}
	`)
	t.Execute(os.Stdout, nil)
}

func demo6(){
	f1 := Friend{Fname: "kobe"}
	f2 := Friend{Fname: "wade"}
	t := template.New("demo6")
	t.Funcs(template.FuncMap{"EmailDeal": EmailDealWith})
	t, _ = t.Parse(`hello {{.UserName}}!
			{{range .Emails}}
				an email {{. | EmailDeal}}
			{{end}}
			{{with .Friends}}
			{{range .}}
				my friend name is {{.Fname}}
			{{end}}
			{{end}}
			`)
	p := Person2{UserName: "zj",
		Emails:  []string{"1@qq.com", "2@qq.com"},
		Friends: []*Friend{&f1, &f2}}

	t.Execute(os.Stdout, p)

	/* 内置模板函数
	var builtins = FuncMap{
		"and":      and,
		"call":     call,
		"html":     HTMLEscaper,
		"index":    index,
		"js":       JSEscaper,
		"len":      length,
		"not":      not,
		"or":       or,
		"print":    fmt.Sprint,
		"printf":   fmt.Sprintf,
		"println":  fmt.Sprintln,
		"urlquery": URLQueryEscaper,
	}*/
}

func EmailDealWith(args ...interface{}) string {
	ok := false
	var s string
	if len(args) == 1 {
		s, ok = args[0].(string)
	}
	if !ok {
		s = fmt.Sprint(args...)
	}
	// find the @ symbol
	substrs := strings.Split(s, "@")
	if len(substrs) != 2 {
		return s
	}
	// replace the @ by " at "
	return (substrs[0] + " at " + substrs[1])
}

func demo7() {
	s1, _ := template.ParseFiles("header.html", "content.html", "footer.html")
	s1.ExecuteTemplate(os.Stdout, "header", nil)
	fmt.Println("**********************")
	s1.ExecuteTemplate(os.Stdout, "content", nil)
	fmt.Println()
	s1.ExecuteTemplate(os.Stdout, "footer", nil)
	fmt.Println()

	s1.Execute(os.Stdout, nil)

}

