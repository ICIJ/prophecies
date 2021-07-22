import isFunction from 'lodash/isFunction'

export default ({ router, store, config, setPageTitle }) => {
  async function setPageTitleFromMeta ({ meta }, from, next) {
    const params = { router, store, config }
    const title = isFunction(meta.title) ? await meta.title(params) : meta.title
    setPageTitle(title)
    next()
  }

  router.beforeEach(setPageTitleFromMeta)
}
