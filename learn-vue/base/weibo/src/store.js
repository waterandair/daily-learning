import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        is_login: false,
        posts_count: 0,
        follows_count: 0,
        fans_count: 0,
        messages_count: 0,
    },
    mutations: {
        updateIsLogin(state, is_login) {
            state.is_login = is_login
        },
        updatePostsCount(state, posts_count) {
            state.posts_count = posts_count
        },
        updateFollowsCount(state, follows_count) {
            state.follows_count = follows_count
        },
        updateFansCount(state, fans_count) {
            state.fans_count = fans_count
        },
        updateMessagesCount(state, messages_count) {
            state.messages_count = messages_count
        },

    },
})
