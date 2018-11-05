package services

import (
	"log"
	"strconv"

	"weibo"

	"github.com/go-redis/redis"
	"github.com/jinzhu/gorm"
)

/* 微博模块 服务 */
type PostService struct {
	db    *gorm.DB
	redis *redis.Client
}

/* 新建服务 */
func NewPostService(db *gorm.DB, redis *redis.Client) *PostService {
	return &PostService{
		db:    db,
		redis: redis,
	}
}

/* 写微博 */
func (ps *PostService) Create(post *weibo.Post) error {
	err := ps.db.Create(&post).Error
	if err == nil {
		// redis 增加微博数
		ps.IncrPostsCountToRedis(post.UserId)
	}
	return err
}

/* 微博列表 */
func (ps *PostService) List(offset, limit uint64) (posts []weibo.Post, err error) {
	if err := ps.db.Offset(offset).Limit(limit).Order("id desc").Find(&posts).Error; err != nil {
		return posts, err
	}

	return posts, nil
}

/* 获取微博总数 */
func (ps *PostService) CountAll() uint64 {
	var count uint64
	err := ps.db.Model(&weibo.Post{}).Count(&count).Error
	if err != nil {
		log.Println(err.Error())
	}

	return count
}

/* 获取个人微博数 */
func (ps *PostService) GetPostsCountByUserId(userId uint64) (uint64, error) {
	var count uint64

	count, err := ps.GetPostsCountFromRedis(userId)
	if err == nil {
		return count, err
	}
	log.Println(err)

	err = ps.db.Model(&weibo.Post{}).Where("user_id = ?", userId).Count(&count).Error
	if err != nil {
		log.Println(err.Error())
	}
	return count, err
}

/* redis 获取微博数 */
func (ps *PostService) GetPostsCountFromRedis(userId uint64) (uint64, error) {
	postsCountKey := "user:id:" + strconv.FormatUint(userId, 10) + ":posts"
	ps.redis.SetNX(postsCountKey, 0, 0)
	postsCount, err := ps.redis.Get(postsCountKey).Uint64()
	if err != nil {
		log.Println(err)
	}

	return postsCount, err
}

/* redis 增加微博数 */
func (ps *PostService) IncrPostsCountToRedis(userId uint64) error {
	postsCountKey := "user:id:" + strconv.FormatUint(userId, 10) + ":posts"
	ps.redis.SetNX(postsCountKey, 0, 0)
	if _, err := ps.redis.Incr(postsCountKey).Result(); err != nil {
		return err
	}
	return nil
}
