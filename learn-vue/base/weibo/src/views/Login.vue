<template>
    <div class="login">
        <form method="post" name="login">
            用户名： <input v-model="username"  /><br>
            密码： <input :type="'password'" v-model="password" />
            <button v-on:click.stop.prevent="login">登录</button>
        </form>
    </div>
</template>

<script>
    import {mapState, mapMutations} from 'vuex'
    export default {
        name: "Login",
        data: function(){
            return {
                username: "",
                password: "",
            }
        },
        methods: {
            login: function () {
                let api_login = "http://localhost:8000/v1/login";
                this.$http.post(api_login, {
                    username: this.username,
                    password: this.password,

                }).then(response => {
                    if(response.data.code == 0) {
                        alert("登录成功");
                        this.updateIsLogin(true);
                        this.$router.push({path: "/"})
                    }
                })
            },
            ...mapMutations(["updateIsLogin"]),
        },
        computed: {
            ...mapState(['is_login']),
        },
    }
</script>

<style scoped>

</style>