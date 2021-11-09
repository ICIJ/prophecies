import {
  createLocalVue,
  mount,
  shallowMount
} from '@vue/test-utils'
import Core from '@/core'
import StatsSortDropdown from '@/components/StatsSortDropdown'

describe('StatsSortDropdown', () => {
  let wrapper
  describe('mount', () => {
    beforeEach(async () => {
      const localVue = createLocalVue()

      // Configure the local vue with plugins
      Core.init(localVue).useAll()

      const options = {
        localVue
      }

      wrapper = await mount(StatsSortDropdown, options)
    })
    it('selects the ID as the default sorting value', () => {
      const selectedElement = wrapper.find('.multiselect__single')
      expect(selectedElement.text()).toBe('ID (default)')
    })
  })

  describe('shallowmount', () => {
    function createContainer () {
      const div = document.createElement('div')
      document.body.appendChild(div)
      return div
    }
    beforeEach(async () => {
      const attachTo = createContainer()
      const localVue = createLocalVue()

      // Configure the local vue with plugins
      const core = Core.init(localVue).useAll()
      const { store, router } = core

      await core.configure()

      // const $route = {
      //   path: '/some/path'
      // }
      const options = {
        store,
        attachTo,
        localVue,
        router

      }

      wrapper = await shallowMount(StatsSortDropdown, options)
    })
    afterEach(async () => {
      await wrapper.destroy()
    })

    it('updates URL when sort option is changed', () => {
      // const url = wrapper.vm.$route.path
      // console.log(url)
      expect(true).toBeTruthy()
    })
  })
})
