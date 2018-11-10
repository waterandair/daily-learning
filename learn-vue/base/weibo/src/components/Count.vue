<template>
    <div class="count">
        <p>
            <span class="posts_count">你好{{ user_name }}</span>
            <span class="posts_count">微博 {{ user_name }}</span>
            <span class="follows_count">关注 {{ user_name }}</span>
            <span class="fans_count">粉丝 {{ user_name }}</span>
            <a class="message">消息</a> <span class="messages_count"> {{ user_name }}</span></p>
        <p><span class="create_post"> <a href="/v1/post/create">写微博</a></span></p>
    </div>
</template>

<script>
    export default {
        name: "Count",
        data: function(){
            return {
                user_name : "zj"
            }
        },
    }
</script>

<style scoped>

</style>