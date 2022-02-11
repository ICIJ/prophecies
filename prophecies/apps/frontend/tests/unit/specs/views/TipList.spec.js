import { createLocalVue, mount } from '@vue/test-utils'

import '@/store'
import Core from '@/core'
import User from '@/models/User'
import TipList from '@/views/TipList'
import TipCard from '@/components/TipCard'

describe('Tip list', () => {
  let wrapper
  function createContainer () {
    const div = document.createElement('div')
    document.body.appendChild(div)
    return div
  }
  beforeAll(async () => {
    await User.api().get()
  })

  beforeEach(async () => {
    const attachTo = createContainer()

    const localVue = createLocalVue()
    // Configure the local vue with plugins
    const stubs = ['app-sidebar', 'app-header', 'latest-tips-card', 'tip-list-page-params']

    const { i18n, wait, store, router } = Core.init(localVue).useAll()

    wrapper = mount(TipList, {
      attachTo,
      i18n,
      localVue,
      router,
      store,
      stubs,
      wait
    })
    await wrapper.vm.setup()
  })

  // afterEach(async () => {
  //   // Prevent a Vue warning in the next tick when the parentNode doesnt exist:
  //   // > TypeError: Cannot read property 'createElement' of null
  //   // @see https://stackoverflow.com/a/62262333
  //   await wrapper.destroy()
  // })

  it('should display list of tips', () => {
    const tipitems = wrapper.findAllComponents(TipCard)
    expect(tipitems).toHaveLength(7)
  })
  it('filter tip list on project id 1', async () => {
    await wrapper.setData({ query: { 'filter[project]': '1' } }) // aladdin project id
    const tipitems = wrapper.findAllComponents(TipCard)
    expect(tipitems).toHaveLength(3)
  })
})
