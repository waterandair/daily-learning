<template>
    <div class="create-post">
        <form method="post" name="create">
            <textarea v-model="content"></textarea>
            <button v-on:click.stop.prevent="create_post">提交{{ content }}</button>
        </form>
    </div>
</template>

<script>
    export default {
        name: "PostCreate",
        data: function(){
            return {
                content: "new post",
            }
        },
        methods: {
            create_post: function () {
                console.log(this.content)
                let api_create_post = "http://localhost:8000/v1/post/create";
                this.$http.post(api_create_post, {
                    content: this.content,
                }).then(response => {
                    if(response.data.code == 0) {
                        alert("提交成功");
                        this.$router.push({path: "/"})
                    }
                })
            },
        },
    }

</script>

<style scoped>

</style>