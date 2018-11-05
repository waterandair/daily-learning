package services

import (
	"log"
	"strconv"

	"weibo"

	"github.com/go-redis/redis"
	"github.com/jinzhu/gorm"
)

/* 关注模块 服务 */
type FollowService struct {
	db    *gorm.DB
	redis *redis.Client
}

/* 新建服务 */
func NewFollowService(db *gorm.DB, redis *redis.Client) *FollowService {
	return &FollowService{
		db:    db,
		redis: redis,
	}
}

/* 添加数据库 follows 记录 */
func (fs *FollowService) Follow(follow *weibo.Follow) error {
	err := fs.db.Create(follow).Error
	if err == nil {
		// redis 增加关注数
		fs.IncrFollowsCountToRedis(follow.UserId)
		// redis 增加粉丝数
		fs.IncrFansCountToRedis(follow.FollowedUserId)
	}
	return err
}

/* 检查是否已经关注过 */
func (fs *FollowService) CheckFollowed(userId, followedUserId uint64) bool {
	count := 0
	if err := fs.db.Model(&weibo.Follow{}).Where("user_id = ? AND followed_user_id = ? ", userId, followedUserId).Count(&count).Error; err != nil {
		log.Println(err)
	}

	if count > 0 {
		return false
	} else {
		return true
	}
}

/* 获取用户的关注数 */
func (fs *FollowService) GetFollowCount(userId uint64) (uint64, error) {
	var count uint64
	count, err := fs.GetFollowsCountFromRedis(userId)
	if err == nil {
		return count, err
	}

	err = fs.db.Model(&weibo.Follow{}).Where("user_id = ?", userId).Count(&count).Error
	if err != nil {
		log.Println(err.Error())
	}
	return count, err
}

/* 获取用户的粉丝数 */
func (fs *FollowService) GetFansCount(userId uint64) (uint64, error) {
	var count uint64
	count, err := fs.GetFansCountFromRedis(userId)
	if err == nil {
		return count, err
	}
	err = fs.db.Model(&weibo.Follow{}).Where("followed_user_id = ?", userId).Count(&count).Error
	if err != nil {
		log.Println(err.Error())
	}
	return count, err
}

// redis 获取关注者数
func (fs *FollowService) GetFollowsCountFromRedis(userId uint64) (uint64, error) {
	followsCountKey := "user:id:" + strconv.FormatUint(userId, 10) + ":follows"
	fs.redis.SetNX(followsCountKey, 0, 0)

	followsCount, err := fs.redis.Get(followsCountKey).Uint64()

	return followsCount, err
}

/*  redis 获取粉丝数 */
func (fs *FollowService) GetFansCountFromRedis(userId uint64) (uint64, error) {
	fansCountKey := "user:id:" + strconv.FormatUint(userId, 10) + ":fans"
	fs.redis.SetNX(fansCountKey, 0, 0)

	fansCount, err := fs.redis.Get(fansCountKey).Uint64()
	if err != nil {
		log.Println(err)
	}

	return fansCount, err
}

/* 增加关注者数 */
func (fs *FollowService) IncrFollowsCountToRedis(userId uint64) error {
	followsCountKey := "user:id:" + strconv.FormatUint(userId, 10) + ":follows"
	fs.redis.SetNX(followsCountKey, 0, 0)
	if _, err := fs.redis.Incr(followsCountKey).Result(); err != nil {
		return err
	}
	return nil
}

/* 增加粉丝数 */
func (fs *FollowService) IncrFansCountToRedis(userId uint64) error {
	fansCountKey := "user:id:" + strconv.FormatUint(userId, 10) + ":fans"
	fs.redis.SetNX(fansCountKey, 0, 0)
	if _, err := fs.redis.Incr(fansCountKey).Result(); err != nil {
		return err
	}
	return nil
}
