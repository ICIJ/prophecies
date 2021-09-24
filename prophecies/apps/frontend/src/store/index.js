import some from 'lodash/some'

import Vue from 'vue'
import Vuex from 'vuex'
import VuexORM from '@vuex-orm/core'
import Cookies from 'js-cookie'

import createPersistedState from 'vuex-persistedstate'

import { database } from '@/store/orm'
import app from './modules/app'

Vue.use(Vuex)

Vue.config.productionTip = process.env.NODE_ENV === 'development'
Vue.config.devtools = process.env.NODE_ENV === 'development'

export default new Vuex.Store({
  modules: {
    app
  },
  strict: process.env.NODE_ENV === 'development',
  plugins: [
    // Instance the ORM database using VuexORM
    VuexORM.install(database),
    // Select which store module should be persisted with local storage
    createPersistedState({
      paths: [
        'app.redirectAfterLogin'
      ],
      filter (mutation) {
        // Only for some mutations
        return some(['app/'], k => mutation.type.indexOf(k) === 0)
      }
    }),
    createPersistedState({
      storage: {
        getItem: key => Cookies.get(key),
        setItem: (key, value) => Cookies.set(key, value, { expires: 365, sameSite: 'lax' }),
        removeItem: key => Cookies.remove(key)
      },
      paths: [
        'app.showTutorial'
      ],
      filter (mutation) {
        // Only for some mutations
        return some(['app'], k => mutation.type.indexOf(k) === 0)
      }
    })
  ]
})
