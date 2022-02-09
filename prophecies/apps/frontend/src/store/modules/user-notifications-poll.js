import { isFunction } from 'lodash'
import UserNotification from '@/models/UserNotification'

export const state = () => ({
  pollId: null,
  fetchs: 0
})

export const mutations = {
  setPollInterval (state, callback) {
    if (isFunction(callback)) {
      state.pollId = setInterval(callback, 1e4)
    }
  },
  clearPollInterval (state) {
    if (state.pollId) {
      clearInterval(state.pollId)
    }
  },
  fetched (state) {
    state.fetchs++
  }
}

export const actions = {
  async fetch ({ commit }) {
    const pageSize = 50
    const include = 'action.actionObject'
    const params = { 'page[size]': pageSize, include }
    // This populates the store automaticaly with Vuex ORM
    await UserNotification.api().get('', { params })
    // Count how many time the notifications are fetched
    commit('fetched')
  },
  startPollAndFetch ({ dispatch }) {
    dispatch('startPoll')
    return dispatch("fetch")
  },
  startPoll({ commit, dispatch, state }) {
    if (!state.pollId) {
      commit("setPollInterval", () => dispatch("fetch"))
    }
  },
  clearPoll({ commit }) {
    commit("clearPollInterval")
  }
}

export const getters = {
  fetched (state) {
    return state.fetchs > 0
  }
}

export default {
  namespaced: true,
  actions,
  getters,
  mutations,
  state
}
