package main

func main() {
	router := initRouter()


	router.Run(":8000")
}