<template>
    <div class="register">
        <form method="post" name="register">
            用户名: <input v-model="username" /> <br>
            邮箱： <input v-model="email" /><br>
            密码： <input v-model="password" :type="'password'" value="" />
            <button v-on:click.stop.prevent="register">注册</button>
        </form>
    </div>
</template>

<script>
    export default {
        name: "Register",
        data: function () {
            return {
                username: "",
                email: "",
                password: "",
            }
        },
        methods: {
            register: register,
        }
    }

    function register(){
        let api_login = "http://localhost:8000/v1/register";
        this.$http.post(api_login, {
            username: this.username,
            email: this.email,
            password: this.password,

        }).then(response => {
            if(response.data.code == 0) {
                alert("注册成功");
                this.$router.push({path: "/login"})
            }
        })
    }
</script>

<style scoped>

</style>