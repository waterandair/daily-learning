package service
// 复杂的业务逻辑不写到 handler 中

import (
	"apiserver/model"
	"sync"
	"apiserver/util"
	"fmt"
)

func ListUser(username string, offset, limit int)([]*model.UserInfo, uint64, error) {
	infos := make([]*model.UserInfo, 0)
	users, count, err := model.ListUser(username, offset, limit)
	if err != nil {
		return nil, count, err
	}

	ids := []uint64{}
	for _, user := range users {
		ids = append(ids, user.Id)
	}

	wg := sync.WaitGroup{}  // 等待一批 goroutine 执行结束
	userList := model.UserList{
		Lock: new(sync.Mutex),
		IdMap: make(map[uint64]*model.UserInfo, len(users)),
	}

	errChan := make(chan error, 1)
	finished := make(chan bool, 1)

	// 并行提高查询效率
	// 在实际业务中,取出数据可能还要对数据进行处理在返回给客户端,这时候为了提高效率,可以并行处理每条数据,待所有并行程序执行完后,在按照id重新排列顺序返回
	for _, u := range users {
		wg.Add(1)  // 添加 goroutine 的个数
		go func(u *model.UserModel) {
			defer wg.Done()  // Done 执行一次 WaitGroup 中需要等待的 goroutine 数量减 1

			shortId, err := util.GenShortId()
			if err != nil {
				errChan <- err
				return
			}

			userList.Lock.Lock()
			defer userList.Lock.Unlock()

			userList.IdMap[u.Id] = &model.UserInfo{
				Id:        u.Id,
				Username:  u.Username,
				SayHello:  fmt.Sprintf("Hello %s", shortId),
				Password:  u.Password,
				CreatedAt: u.CreatedAt.Format("2006-01-02 15:04:05"),
				UpdatedAt: u.UpdatedAt.Format("2006-01-02 15:04:05"),
			}
		}(u)
	}

	go func() {
		wg.Wait()
		close(finished)
	}()

	select {
	case <-finished:
	case err:= <-errChan:
		return nil, count, err

	}

	for _, id := range ids {
		infos = append(infos, userList.IdMap[id])
	}

	return infos, count, nil
}
