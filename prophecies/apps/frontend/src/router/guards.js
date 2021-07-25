import isFunction from 'lodash/isFunction'

export default (core) => {
  async function setPageTitleFromMeta ({ meta }, from, next) {
    const params = { router: core.router, store: core.store, config: core.store, i18n: core.i18n }
    const title = isFunction(meta.title) ? await meta.title(params) : meta.title
    core.setPageTitle(title)
    next()
  }

  async function checkUserAuthentication (to, from, next) {
    try {
      // This route doesn't need auth
      // or the user is authenticated
      if (['login', 'error'].includes(to.name) || await core.getUser()) {
        next()
      }
    } catch (error) {
      // The error has a status starting with 40
      if (String(error?.response?.status).startsWith(40)) {
        next({ name: 'login' })
      } else {
        next({ name: 'error', params: { error } })
      }
    }
  }

  core.router.beforeEach(setPageTitleFromMeta)
  core.router.beforeEach(checkUserAuthentication)
}
