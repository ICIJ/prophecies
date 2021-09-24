export const state = () => ({
  redirectAfterLogin: null,
  showTutorial: null
})

export const mutations = {
  setRedirectAfterLogin (state, path = null) {
    if (!path || !path.startsWith('/login')) {
      state.redirectAfterLogin = path
    }
  },
  setShowTutorial (state, showTutorial) {
    state.showTutorial = showTutorial
  }
}

export const actions = {
  popRedirectAfterLogin ({ state: { redirectAfterLogin }, commit }) {
    commit('setRedirectAfterLogin', null)
    return redirectAfterLogin
  },
  showTutorial ({ state: { showTutorial }, commit }, isShown) {
    commit('setShowTutorial', isShown)
    return showTutorial
  }
}

export default {
  namespaced: true,
  actions,
  mutations,
  state
}
