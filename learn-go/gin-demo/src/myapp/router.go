package main

import (
	"github.com/gin-gonic/gin"
	"myapp/apis"
)

func initRouter() *gin.Engine {
	router := gin.Default()
	router.GET("/", apis.IndexApi)
	// curl -X POST http://127.0.0.1:8000/person -d "first_name=zj&last_name=zj"
	router.POST("/person", apis.AddPersonApi)
	// curl  http://127.0.0.1:8000/persons | python -m json.tool
	router.GET("/persons", apis.GetPersonsApi)
	// curl  http://127.0.0.1:8000/person/1
	router.GET("/person/:id", apis.GetPersonApi)
	//  curl -X PUT http://127.0.0.1:8000/person/2 -d "first_name=noldor&last_name=elves"
	// curl -X PUT http://127.0.0.1:8000/person/2 -H "Content-Type: application/json"  -d '{"first_name": "vanyar", "last_name": "elves"}'
	router.PUT("/person/:id", apis.ModPersonApi)
	// curl -X DELETE http://127.0.0.1:8000/person/2
	router.DELETE("/person/:id", apis.DelPersonApi)

	return router
}
