package main

import (
	"github.com/gin-gonic/gin"
	"net/http"
	"fmt"
	"os"
	"log"
	"io"
	"time"
	"strconv"
)

func QueryBody(c *gin.Context) {
	a := c.PostForm("a")
	b := c.DefaultPostForm("b", "b")

	cc := c.Query("c")

	params := c.Param("params")

	var p Person
	c.Bind(&p)

	c.JSON(http.StatusOK, gin.H{
		"a": a,
		"b": b,
		"c": cc,
		"params": params,
		"person": gin.H{
			"name": p.Name,
			"age": p.Age,
		},
	})



}

func UploadFile(c *gin.Context) {
	file, header, err := c.Request.FormFile("upload")
	if err != nil {
		c.String(http.StatusBadRequest, "Bad Request")
		return
	}
	filename := header.Filename
	fmt.Println(file, err, filename)
	path := "./pictures/"
	os.Mkdir(path, 0777)
	out, err := os.Create(path + strconv.FormatInt(time.Now().Unix(), 10) +filename )
	if err != nil {
		log.Fatal(err)
	}
	defer out.Close()

	_, err = io.Copy(out, file)
	if err != nil {
		log.Fatal(err)
	}
	c.String(http.StatusCreated, "upload success")
}

func UploadFiles(c *gin.Context) {
	err := c.Request.ParseMultipartForm(200000)
	if err != nil {
		log.Fatal()
	}

	files := c.Request.MultipartForm.File["uploads"]

	for i, _ := range files {
		file, err := files[i].Open()
		if err != nil {
			log.Fatal(err)
		}

		out, err := os.Create("./pictures/" + strconv.FormatInt(time.Now().Unix(), 10) + files[i].Filename)
		defer out.Close()

		if err != nil {
			log.Fatal(err)
		}

		_, err = io.Copy(out, file)
		if err != nil {
			log.Fatal(err)
		}

		c.String(http.StatusCreated, "uploads successful")
	}
}

