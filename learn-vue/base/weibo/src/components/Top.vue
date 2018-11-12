<template>
    <div class="header">
        <a>
            <img v-on:click="go_index" class="logo" src="../assets/logo.png"/>
        </a>
        <div class="header-r">
            <div v-if="this.is_login == true" class="greetings">你好 <span>zj</span></div>
            <div v-if="this.is_login == true" class="counts">
                <ul class="counts_list">
                    <li><span>微博：{{ this.posts_count }}</span></li>
                    <li><span>关注：{{ this.follows_count }}</span></li>
                    <li><span>粉丝：{{ this.fans_count }}</span></li>
                    <li><span>消息：<a class="message_count" v-on:click.stop="go_messages" href="#">{{ this.messages_count }}</a></span>
                    </li>
                </ul>
            </div>
            <div class="login">
                <ul class="gn_login_list">
                    <li>
                        <button v-if="this.is_login == false && this.$route.name != 'login' " v-on:click="login">登录
                        </button>
                    </li>
                    <li>
                        <button v-if="this.is_login == false && this.$route.name != 'register'" v-on:click="register">
                            注册
                        </button>
                    </li>
                    <li>
                        <button v-if="this.is_login == true" v-on:click="logout">退出</button>
                    </li>
                    <li>
                        <button v-if="this.is_login == true" v-on:click="post_create">写微博</button>
                    </li>

                </ul>
            </div>
        </div>
    </div>
</template>

<script>
    import {mapState, mapMutations} from 'vuex'

    export default {
        name: "Top",
        methods: {
            ...mapMutations(["updateIsLogin"]),
            login: login,
            register: register,
            logout: logout,
            post_create: post_create,
            go_index: go_index,
            go_messages: go_messages,

        },
        computed: mapState(['is_login', "posts_count", "follows_count", "fans_count", "messages_count"])
    }

    // 跳转到登录
    function login() {
        this.$router.push({path: "/login"})
    }

    // 跳转到注册
    function register() {
        this.$router.push({path: "/register"})
    }

    // 退出
    function logout() {
        this.updateIsLogin(false)
        document.cookie = "Authorization" + "=" + "; expires=Thu, 01-Jan-70 00:00:01 GMT";
        window.location.reload()
    }

    // 写微博
    function post_create() {
        this.$router.push({path: "/post/create"})
    }

    // 去首页
    function go_index() {
        this.$router.push({path: "/"})
    }

    // 跳转到消息页
    function go_messages(event) {
        let nums = event.target.text
        let path = '/messages/' + nums

        this.$router.push({path: path})
    }
</script>

<style scoped>
    .header {
        width: 100%;
        height: 48px;
        border-top: 2px solid #fa7d3c;
        box-shadow: 0 0 1px 0px rgba(0, 0, 0, 0.15);
        background: #fff;
        line-height: 48px;
    }

    .logo {
        cursor: pointer;
        margin-left: 40px;
        width: 140px;
        height: 48px;
        float: left;
    }

    .greetings, .counts {
        float: left;
        padding-right: 60px;
    }

    .counts li {
        float: left;
        padding-right: 20px;
    }

    .login {
        float: right;
    }

    .login li {
        float: right;
        padding-right: 20px;
    }

    .header-r {
        width: 900px;
        float: right;
        height: 48px;
    }

    button {
        font-size: 14px;
        padding: 0 10px;
        height: 28px;
        line-height: 28px;
        text-align: center;
        margin-left: 20px;
        color: white;
        background-color: #3BD9FF;
        border-radius: 6px;
        border: 0;
        cursor: pointer;
    }

    .message_count {
        text-decoration: underline;
        color: blue;
    }
</style>