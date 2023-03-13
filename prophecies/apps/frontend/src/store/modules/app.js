export const state = () => ({
  redirectAfterLogin: null,
  showTutorial: true,
  locale: 'en'
})

export const mutations = {
  setRedirectAfterLogin(state, path = null) {
    if (!path || !path.startsWith('/login')) {
      state.redirectAfterLogin = path
    }
  },
  setShowTutorial(state, showTutorial) {
    state.showTutorial = showTutorial
  },
  setLocale(state, locale) {
    state.locale = locale
  }
}

export const actions = {
  popRedirectAfterLogin({state: {redirectAfterLogin}, commit}) {
    commit('setRedirectAfterLogin', null)
    return redirectAfterLogin
  },
  showTutorial({state: {showTutorial}, commit}, isShown) {
    commit('setShowTutorial', isShown)
    return showTutorial
  },
  locale({commit}, locale) {
    commit('setLocale', locale)
  }
}

export default {
  namespaced: true,
  actions,
  mutations,
  state
}
