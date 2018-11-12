<template>
    <div class="center">
        <div class="posts">
            <ul>
                <li v-for="(post) in posts" :key="post.id" :data-id="post.id" class="post">
                    <div>
                        <div class="post_title">
                            <span class="face"><img src="../assets/face.jpg" style="border-radius: 50%;" width="20"
                                                    height="20" alt=""></span>
                            <span class="username">{{ post.user_name }}</span>
                            <button class="follow" v-on:click.stop="follow" :data-user-id="post.user_id"
                                    v-if="user_id != post.user_id">关注
                            </button>
                        </div>
                        <div class="post_content">
                            {{ post.content }}
                        </div>
                        <div class="like">
                            <span v-bind:id="'likes-count-'+ post.id">{{ likes_counts[post.id] }}</span>
                            <span>热度: </span>
                            <button v-if="user_id != post.user_id" v-on:click.stop="like" :data-user-id="post.user_id"
                                    :data-post-id="post.id">赞
                            </button>
                        </div>

                    </div>
                </li>
            </ul>
        </div>

    </div>
</template>

<script>
    import {mapState, mapMutations} from 'vuex'

    export default {
        name: "PostList",
        data: function () {
            return {
                posts: {},
                likes_counts: {},
                user_id: 0,
                user_name: "",
                message_url: '',
                current_page: 1,
                page_count: 1,
            }
        },

        mounted() {
            let api_post_list = 'http://localhost:8000/v1/';
            let page = 1
            this.$http.post(api_post_list, {
                page: page
            }).then(response => {
                this.posts = response.data.data.posts
                this.likes_counts = response.data.data.likes_counts
                this.user_id = response.data.data.user_id
                this.user_name = response.data.data.user_name
                this.message_url = response.data.data.message_url
                this.current_page = response.data.data.current_page
                this.page_count = response.data.data.page_count

                this.updateIsLogin(response.data.data.is_login)

                this.updatePostsCount(response.data.data.posts_count)
                this.updateFollowsCount(response.data.data.follows_count)
                this.updateFansCount(response.data.data.fans_count)
                this.updateMessagesCount(response.data.data.messages_count)
            })
        },

        computed: {
            ...mapState(['is_login', 'posts_count', 'follows_count', 'fans_count', 'messages_count']),
        },
        methods: {
            ...mapMutations(["updateIsLogin", "updatePostsCount", "updateFollowsCount", "updateFansCount", "updateMessagesCount"]),
            follow: function (event) {
                let api_follow = "http://localhost:8000/v1/follow"
                this.$http.post(api_follow, {
                    followed_user_id: parseInt(event.target.getAttribute('data-user-id'))
                }).then(response => {
                    if (response.data.code == 0) {
                        this.updateFollowsCount(this.follows_count + 1)
                        alert("关注成功");
                        this.$router.push({path: "/"})
                    } else {
                        alert("code:" + response.data.code + " message:" + response.data.message + response.data.data);
                    }
                })
            },

            like: function (event) {
                let api_like = "http://localhost:8000/v1/like"

                this.$http.post(api_like, {
                    to_user_id: parseInt(event.target.getAttribute('data-user-id')),
                    post_id: parseInt(event.target.getAttribute("data-post-id"))
                }).then(response => {
                    if (response.data.code == 0) {
                        let post_id = event.target.getAttribute("data-post-id");
                        let key = "likes-count-" + post_id;
                        let likes_count = document.getElementById(key).textContent;
                        document.getElementById(key).textContent = parseInt(likes_count) + 1;
                        alert("点赞成功");
                    } else {
                        alert("code:" + response.data.code + "  message:" + response.data.message + response.data.data);
                    }
                })
            }
        }
    }
</script>

<style scoped>
    .posts {
        width: 960px;
        margin: 20px auto;
    }

    .posts button {
        margin-top: 4px;
    }

    .post {
        display: block;
        border: 1px solid #e5e5e5;
        margin-bottom: 10px;
        padding-bottom: 10px;
    }

    .post_title {
        width: 200px;
        height: 30px;
        line-height: 30px;
        padding-left: 10px;
        border-bottom: 1px solid #e5e5e5;
    }

    .face {
        position: relative;
    }

    .face img {
        position: absolute;
        bottom: -1px;
    }

    .post .username, .follow {
        margin-left: 26px;
    }

    .post_content {
        width: 400px;
        word-wrap: break-word;
        border-bottom: 1px solid #e5e5e5;
        padding: 10px 20px;
    }

    .like {
        clear: both;
        width: 400px;
        height: 20px;
        line-height: 20px;
    }

    .like span, button {
        float: right;
        margin-right: 20px;
        margin-top: 8px;
    }
</style>