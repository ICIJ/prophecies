import some from 'lodash/some'

import Vue from 'vue'
import Vuex from 'vuex'
import createPersistedState from 'vuex-persistedstate'

import app from './modules/app'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    app
  },
  strict: process.env.NODE_ENV === 'development',
  plugins: [
    createPersistedState({
      paths: [
        'app.redirectAfterLogin'
      ],
      filter (mutation) {
        // Only for some mutations
        return some(['app/'], k => mutation.type.indexOf(k) === 0)
      }
    })
  ]
})
