<template>
    <!--<div class="register">-->
    <!--<form method="post" name="register">-->
    <!--用户名: <input v-model="username" /> <br>-->
    <!--邮箱： <input v-model="email" /><br>-->
    <!--密码： <input v-model="password" :type="'password'" value="" />-->
    <!--<button v-on:click.stop.prevent="register">注册</button>-->
    <!--</form>-->
    <!--</div>-->

    <div id="login_frame">
        <form method="post" name="register">

            <p><label>用户名: </label><input v-model="username" class="text_field"/></p>
            <p><label>&nbsp;&nbsp;&nbsp;&nbsp;邮箱: </label><input v-model="email" class="text_field"/></p>
            <p><label>&nbsp;&nbsp;&nbsp;&nbsp;密码: </label><input :type="'password'" v-model="password"
                                                                 class="text_field"/></p>

            <div class="login_control">
                <button class="login_button" v-on:click.stop.prevent="register">注册</button>
                <button class="login_button" v-on:click.stop.prevent="login">已有账号去登录</button>
            </div>
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
            login: login,
        }
    }

    function register() {
        let api_login = "http://localhost:8000/v1/register";
        this.$http.post(api_login, {
            username: this.username,
            email: this.email,
            password: this.password,

        }).then(response => {
            if (response.data.code == 0) {
                alert("注册成功");
                this.$router.push({path: "/login"})
            } else {
                alert("code:" + response.data.code + "  message:" + response.data.message + response.data.data);
            }
        })
    }

    function login() {
        this.$router.push("/login")
    }
</script>

<style scoped>
    #login_frame {
        width: 400px;
        height: 260px;
        padding: 16px;

        position: absolute;
        left: 50%;
        top: 50%;
        margin-left: -200px;
        margin-top: -100px;

        border-radius: 10px;
        text-align: center;
    }

    #login_frame p {
        margin-top: 20px;
    }

    .text_field {
        width: 278px;
        height: 28px;
        border-top-right-radius: 5px;
        border-bottom-right-radius: 5px;
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

    .login_control {
        margin-left: 50px;
        margin-top: 20px;
        padding: 0 28px;
    }
</style>