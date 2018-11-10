<template>
    <div class="center">
        <div class="count">
            <div>
                <p>你好 <span class="posts_count">{{ user_name }}</span></p>
            </div>
            <div>
                <p>微博 <span class="posts_count">{{ posts_count }}</span></p>
            </div>
            <div>
                <p>关注 <span class="follows_count">{{ follows_count }}</span></p>
            </div>
            <div>
                <p>粉丝 <span class="fans_count">{{ fans_count }}</span></p>
            </div>
            <div>
                <p><a :href="message_url" class="message">消息</a> <span
                        class="messages_count"> {{ messages_count }}</span></p>
            </div>
        </div>
        <div class="post">
            <ul>
                <li v-for="(post) in posts" :key="post.id" :data-id="post.id" class="post">
                    <div style="border: black;border-style: solid">
                        <div>
                            用户名: {{ post.user_name }}
                            <button v-on:click.stop="follow" :data-user-id="post.user_id" v-if="user_id != post.user_id">关注</button>
                        </div>
                        <div>
                            内容： {{ post.content }}
                        </div>
                        <div>
                            点赞数: <span v-bind:id="'likes-count-'+ post.id">{{ likes_counts[post.id] }}</span>
                        </div>
                        <div v-if="user_id != post.user_id">
                            <button class="like" v-on:click.stop="like" :data-user-id="post.user_id" :data-post-id="post.id">赞</button>
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
                posts_count: 0,
                follows_count: 0,
                fans_count: 0,
                messages_count: 0,
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
            console.log(this)
            this.$http.post(api_post_list, {
                page: page
            }).then(response => {
                console.log(response.data)
                this.posts_count = response.data.data.posts_count
                this.follows_count = response.data.data.follows_count
                this.fans_count = response.data.data.fans_count
                this.messages_count = response.data.data.messages_count
                this.posts = response.data.data.posts
                this.likes_counts = response.data.data.likes_counts
                this.user_id = response.data.data.user_id
                this.user_name = response.data.data.user_name
                this.message_url = response.data.data.message_url
                this.current_page = response.data.data.current_page
                this.page_count = response.data.data.page_count

                this.updateIsLogin(response.data.data.is_login)
            })
        },

        computed: {
            ...mapState(['is_login']),
        },
        methods: {
            ...mapMutations(["updateIsLogin"]),
            follow : function (event) {
                let api_follow = "http://localhost:8000/v1/follow"
                this.$http.post(api_follow, {
                    followed_id : parseInt(event.target.getAttribute('data-user-id'))
                }).then(response => {
                    if(response.data.code == 0) {
                        console.log(response.data)
                        this.follows_count ++
                        alert("关注成功");
                        this.$router.push({path: "/"})
                    } else {
                        alert("code:" + response.data.code + "  message:" +response.data.message + response.data.data);
                    }
                })
            },
            
            like : function (event) {
                let api_like = "http://localhost:8000/v1/like"

                this.$http.post(api_like, {
                    to_user_id : parseInt(event.target.getAttribute('data-user-id')),
                    post_id : parseInt(event.target.getAttribute("data-post-id"))
                }).then(response => {
                    if(response.data.code == 0) {
                        let post_id = event.target.getAttribute("data-post-id");
                        let key = "likes-count-" + post_id;
                        let likes_count = document.getElementById(key).textContent;
                        document.getElementById(key).textContent = parseInt(likes_count) + 1;
                        alert("点赞成功");
                    } else {
                        alert("code:" + response.data.code + "  message:" +response.data.message + response.data.data);
                    }
                })
            }
        }
    }
</script>

<style scoped>

</style>