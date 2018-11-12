<template>
    <div class="message">
        <ul>
            <li v-for="message in messages" :key="message.id">{{ message.from_user_name }} 刚刚给你的微博点了赞</li>
        </ul>
    </div>
</template>

<script>
    import {mapMutations} from 'vuex'

    export default {
        name: "Message",
        props: ['nums'],
        data: function () {
            return {
                messages: {}
            }
        },
        methods: {
            ...mapMutations(['updateMessagesCount'])
        },
        mounted: function () {
            let nums = this.$route.params.nums
            if (!nums) {
                nums = 0
            }

            let api_get_messages = '/v1/like/' + nums
            this.$http.get(api_get_messages).then(response => {
                if (response.data.code == 0) {
                    this.messages = response.data.data.messages
                } else {
                    console.log("code:" + response.data.code + "  message:" + response.data.message + response.data.data);
                }
            })

            this.updateMessagesCount(0)
        }
    }
</script>

<style scoped>
    .message {
        width: 960px;
        margin: 20px auto;
    }

    .message li {
        border-bottom: 1px solid #e5e5e5;
        margin-bottom: 10px;
    }

</style>