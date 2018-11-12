<template>
    <div class="create-post">
        <form method="post" name="create">
            <textarea v-model="content" rows="5" cols="50"></textarea>
            <div>
                <button class="button" v-on:click.stop.prevent="create_post">提交</button>
            </div>
        </form>
    </div>
</template>

<script>
    export default {
        name: "PostCreate",
        data: function () {
            return {
                content: "new post",
            }
        },
        methods: {
            create_post: function () {
                let api_create_post = "http://localhost:8000/v1/post/create";
                this.$http.post(api_create_post, {
                    content: this.content,
                }).then(response => {
                    if (response.data.code == 0) {
                        alert("提交成功");
                        this.$router.push({path: "/"})
                    } else {
                        alert("code:" + response.data.code + "  message:" + response.data.message + response.data.data);
                    }
                })
            },
        },
    }

</script>

<style scoped>
    .create-post {
        width: 960px;
        margin: 20px auto;
        text-align: center;
    }

    input, textarea {
        padding: 5px;
        font-size: 15px;
        outline: none;
        text-shadow: 0px 1px 0px #fff;
        -webkit-border-radius: 3px;
        -moz-border-radius: 3px;
        border-radius: 3px;
        border: 1px solid #ccc;
        -webkit-transition: .3s ease-in-out;
        -moz-transition: .3s ease-in-out;
        -o-transition: .3s ease-in-out;
    }

    input:focus, textarea:focus {
        border: 1px solid #fafafa;
        -webkit-box-shadow: 0px 0px 6px #007eff;
        -moz-box-shadow: 0px 0px 5px #007eff;
        box-shadow: 0px 0px 5px #007eff;
    }

    .button {
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
</style>