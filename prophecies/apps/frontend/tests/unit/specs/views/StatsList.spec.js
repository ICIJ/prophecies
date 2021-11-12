import {
  createLocalVue,
  mount
} from '@vue/test-utils'
import Core from '@/core'
import StatsList from '@/views/StatsList'

describe('StatsList', () => {
  let wrapper

  beforeEach(async () => {
    const localVue = createLocalVue()
    // Configure the local vue with plugins
    const core = Core.init(localVue).useAll()
    const { wait, store, router, i18n } = core
    const stubs = ['app-waiter']

    const options = {
      stubs,
      localVue,
      store,
      wait,
      i18n,
      router
    }

    await core.configure()
    wrapper = await mount(StatsList, options)
  })
  afterEach(async () => {
    await wrapper.destroy()
  })
  it('Shows sort dropdown', () => {
    const element = wrapper.find('.stats-list__sort-by')
    expect(element.exists()).toBeTruthy()
  })

  it('Update url with sort parameter on sort change', async () => {
    expect(wrapper.vm.sortField).toBe('name_asc')
    wrapper.vm.sortField = 'name_desc'
    await wrapper.vm.$nextTick()
    expect(wrapper.vm.$route.query.sort).toBe('name_desc')
  })
})
