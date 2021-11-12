import {
  createLocalVue,
  shallowMount
} from '@vue/test-utils'
import Core from '@/core'
import StatsList from '@/views/StatsList'

describe('StatsList', () => {
  let wrapper

  beforeEach(async () => {
    const localVue = createLocalVue()
    // Configure the local vue with plugins
    const core = Core.init(localVue).useAll()
    const { wait, store, router } = core
    const stubs = ['app-waiter']

    const options = {
      stubs,
      localVue,
      store,
      wait,
      router
    }

    await core.configure()
    wrapper = await shallowMount(StatsList, options)
  })

  afterEach(async () => {
    await wrapper.destroy()
  })

  it('Shows sort dropdown', () => {
    const element = wrapper.find('sort-by-dropdown-stub')
    expect(element.exists()).toBeTruthy()
  })
})
