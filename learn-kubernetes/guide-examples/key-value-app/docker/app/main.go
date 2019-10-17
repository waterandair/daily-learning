package main

import (
	"encoding/json"
	"io/ioutil"
	"log"
	"net/http"
	"os"

	"github.com/go-redis/redis/v7"
)

type Controller struct {
	masterCli *redis.Client
	slaveCli  *redis.Client
}

type Content struct {
	Key              string `json:"key"`
	Value            string `json:"value"`
	RedisReplication string `json:"redis_replication"`
	Action           string `json:"action"`
	PodIP            string `json:"pod_ip"`
}

// SetKey 设置一个 key
func (c *Controller) SetKey(rw http.ResponseWriter, req *http.Request) {
	body, _ := ioutil.ReadAll(req.Body)
	req.Body.Close()

	content := new(Content)
	if err := json.Unmarshal(body, content); err != nil {
		rw.Write([]byte(err.Error()))
		return
	}

	c.masterCli.Set(content.Key, content.Value, 0)

	content.Action = "SET"
	content.RedisReplication = c.masterCli.Info("Replication").Val()
	content.PodIP = os.Getenv("POD_IP")

	res, _ := json.Marshal(content)
	rw.Write(res)
}

//  GetKey 获取一个 key
func (c *Controller) GetKey(rw http.ResponseWriter, req *http.Request) {
	key := req.URL.Query().Get("key")
	value := c.slaveCli.Get(key).String()

	content := &Content{
		Key:              key,
		Value:            value,
		RedisReplication: c.slaveCli.Info("Replication").Val(),
		Action:           "GET",
		PodIP:            os.Getenv("POD_IP"),
	}

	res, _ := json.Marshal(content)
	rw.Write(res)

}

func main() {
	controller := &Controller{
		masterCli: redis.NewClient(&redis.Options{Addr: "redis-master:6379"}),
		// 这里用域名的方式连接到 redis slave, 这样就可以使用 kubernetes Service 的负载均衡
		slaveCli: redis.NewClient(&redis.Options{Addr: "redis-slave:6379"}),
	}

	http.HandleFunc("/set", controller.SetKey)
	http.HandleFunc("/get", controller.GetKey)
	log.Fatal(http.ListenAndServe(":8082", nil))
}
