import {get, isFunction} from 'lodash'
import UserNotification from '@/models/UserNotification'

export const state = () => ({
  pollId: null,
  fetchedIds: [],
  fetchs: 0
})

export const mutations = {
  setPollInterval(state, callback) {
    if (isFunction(callback)) {
      state.pollId = setInterval(callback, 1e4)
    }
  },
  clearPollInterval(state) {
    if (state.pollId) {
      clearInterval(state.pollId)
    }
  },
  fetched(state) {
    state.fetchs++
  },
  fetchedIds(state, fetchedIds) {
    state.fetchedIds = fetchedIds
  }
}

export const actions = {
  async fetchLatest({commit, dispatch, state}) {
    const pageSize = 1
    const params = {'page[size]': pageSize}
    const save = false
    // This WONT populate the store automaticaly with Vuex ORM
    const {response} = await UserNotification.api().get('', {params, save})
    // Collect the first id in the list of latest ids
    const [latestId = null] = get(response, 'data.data', []).map(n => n.id)
    const [latestStoredId = null] = state.fetchedIds
    // The id is different from the first in the state, we must fetch more
    if (latestId !== latestStoredId) {
      return dispatch('fetch')
    }
    // Count how many time the notifications are fetched
    commit('fetched')
  },
  async fetch({commit}) {
    const pageSize = 50
    const include = 'action.actionObject,action.actor'
    const params = {'page[size]': pageSize, include}
    // This populates the store automaticaly with Vuex ORM
    const {response} = await UserNotification.api().get('', {params})
    // Collect fetched ids
    commit('fetchedIds', get(response, 'data.data', []).map(n => n.id))
    // Count how many time the notifications are fetched
    commit('fetched')
  },
  startPollAndFetch({dispatch}) {
    dispatch('startPoll')
    return dispatch("fetch")
  },
  startPoll({commit, dispatch, state}) {
    if (!state.pollId) {
      commit("setPollInterval", () => dispatch("fetchLatest"))
    }
  },
  clearPoll({commit}) {
    commit("clearPollInterval")
  }
}

export const getters = {
  fetched(state) {
    return state.fetchs > 0
  },
  fetchedIds(state) {
    return state.fetchedIds
  },
  fetchedObjects(state) {
    return UserNotification
      .query()
      .whereIdIn(state.fetchedIds)
      .orderBy('createdAt', 'desc')
      .get()
  }
}

export default {
  namespaced: true,
  actions,
  getters,
  mutations,
  state
}
