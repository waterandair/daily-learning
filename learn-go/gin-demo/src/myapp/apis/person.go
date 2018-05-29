package apis

import (
	"github.com/gin-gonic/gin"
	"net/http"
	. "myapp/models"
	"log"
	"fmt"
	"strconv"
)

func IndexApi(c *gin.Context) {
	c.String(http.StatusOK, "it works")
}

func AddPersonApi(c *gin.Context) {
	firstName := c.Request.FormValue("first_name")
	lastName := c.Request.FormValue("last_name")

	p := Person{FirstName:firstName, LastName:lastName}
	ra, err := p.AddPerson()
	if err != nil {
		log.Fatalln(err)
	}
	msg := fmt.Sprintf("insert successful %d", ra)
	c.JSON(http.StatusOK, gin.H{
		"msg": msg,
	})
}

func GetPersonsApi(c *gin.Context) {
	var p Person
	persons, err := p.GetPersons()
	if err != nil {
		log.Fatalln(err)
	}
	c.JSON(http.StatusOK, gin.H{
		"persons": persons,
	})
}

func GetPersonApi(c *gin.Context) {
	var p Person
	cid := c.Param("id")
	id, err := strconv.Atoi(cid)
	if err != nil {
		log.Fatalln(err)
	}
	p.Id = id
	person, err := p.GetPerson()
	if err != nil {
		log.Fatalln(err)
	}
	c.JSON(http.StatusOK, gin.H{
		"person": person,
	})
}

func ModPersonApi(c *gin.Context) {
	var p Person
	cid := c.Param("id")
	id, err := strconv.Atoi(cid)
	if err != nil {
		log.Fatalln(err)
	}

	p.Id = id
	err = c.Bind(&p)
	if err != nil {
		log.Fatalln(err)
	}

	ra, err := p.UpdatePerson()
	if err != nil {
		log.Fatalln(err)
	}

	msg := fmt.Sprintf("update person successful %d", ra)
	c.JSON(http.StatusOK, gin.H{
		"msg": msg,
	})
}

func DelPersonApi(c *gin.Context) {
	var p Person
	cid := c.Param("id")
	id, err := strconv.Atoi(cid)
	if err != nil {
		log.Fatalln(id)
	}

	p.Id = id
	ra, err := p.DeletePerson()
	if err != nil {
		log.Fatalln(err)
	}
	msg := fmt.Sprintf("delete person seccussful %d", ra)
	c.JSON(http.StatusOK, gin.H{
		"msg": msg,
	})

}