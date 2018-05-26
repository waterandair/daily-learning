package main

import (
	db "myapp/database"
)
func main() {
	defer db.SqlDB.Close()

	router := initRouter()
	router.Run(":8000")
}