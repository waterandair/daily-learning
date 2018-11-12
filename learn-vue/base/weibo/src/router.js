import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'

Vue.use(Router)

export default new Router({
    mode: 'history',
    routes: [
        {
            path: '/',
            name: 'home',
            component: Home
        },
        {
            path: '/login',
            name: 'login',
            component: () => import('./views/Login.vue')
        },
        {
            path: '/register',
            name: 'register',
            component: () => import('./views/Register.vue')
        },
        {
            path: '/post/create',
            name: 'post_create',
            component: () => import('./views/PostCreate.vue')
        },
        {
            path: '/messages/:nums',
            name: 'messages',
            props: true,
            component: () => import('./views/Message.vue')
        },
    ]
})
