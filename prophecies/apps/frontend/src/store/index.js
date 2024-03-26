import some from 'lodash/some'
import Vue from 'vue'
import Vuex from 'vuex'
import VuexORM from '@vuex-orm/core'
import createPersistedState from 'vuex-persistedstate'

import app from './modules/app'
import userNotificationsPoll from './modules/user-notifications-poll'

import { database } from '@/store/orm'

Vue.use(Vuex)

Vue.config.productionTip = process.env.NODE_ENV === 'development'
Vue.config.devtools = process.env.NODE_ENV === 'development'

export function createStore() {
  return new Vuex.Store({
    modules: {
      app,
      userNotificationsPoll
    },
    strict: process.env.NODE_ENV === 'development',
    plugins: [
      // Instance the ORM database using VuexORM
      VuexORM.install(database),
      // Select which store module should be persisted with local storage
      createPersistedState({
        paths: ['app.redirectAfterLogin', 'app.showTutorial', 'app.locale'],
        filter(mutation) {
          // Only for some mutations
          return some(['app/'], (k) => mutation.type.indexOf(k) === 0)
        }
      })
    ]
  })
}

export default createStore()
