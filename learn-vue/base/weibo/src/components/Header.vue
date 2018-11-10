<template>
    <div id="login">
        <button v-if="this.is_login == false && this.$route.name != 'login' " v-on:click="login">登录</button>
        <button v-if="this.is_login == false && this.$route.name != 'register'" v-on:click="register">注册</button>
        <button v-if="this.is_login == true" v-on:click="logout">退出</button>
        <button v-if="this.is_login == true" v-on:click="post_create">写微博</button>
    </div>
</template>

<script>
    import {mapState, mapMutations} from 'vuex'

    export default {
        name: "Header",
        methods: {
            ...mapMutations(["updateIsLogin"]),
            login: login,
            register: register,
            logout: logout,
            post_create: post_create,

        },
        computed: mapState(['is_login'])
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
</script>

<style scoped>

</style>