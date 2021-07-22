export const state = () => ({
  redirectAfterLogin: null
})

export const mutations = {
  setRedirectAfterLogin (state, path = null) {
    if (!path || !path.startsWith('/login')) {
      state.redirectAfterLogin = path
    }
  }
}

export const actions = {
  popRedirectAfterLogin ({ state: { redirectAfterLogin }, commit }) {
    commit('setRedirectAfterLogin', null)
    return redirectAfterLogin
  }
}

export default {
  namespaced: true,
  actions,
  mutations,
  state
}
