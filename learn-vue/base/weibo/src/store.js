import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
      is_login: false
  },
  mutations: {
      updateIsLogin(state, is_login) {
          state.is_login = is_login
      },
  },
})
