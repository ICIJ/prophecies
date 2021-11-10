import {
  createLocalVue,
  mount,
  shallowMount
} from '@vue/test-utils'
import Core from '@/core'
import SortByDropdown from '@/components/SortByDropdown'

describe('SortByDropdown', () => {
  let wrapper
  describe('mount', () => {
    beforeEach(async () => {
      const localVue = createLocalVue()

      // Configure the local vue with plugins
      Core.init(localVue).useAll()
      const propsData = {
        sort: 'task_id',
        options: [
          { value: 'task_id', label: 'ID (default)', $isDefault: true }
        ]
      }
      const options = {
        localVue,
        propsData
      }

      wrapper = await mount(SortByDropdown, options)
    })
    it('selects the ID as the default sorting value', () => {
      const selectedElement = wrapper.find('.multiselect__single')
      expect(selectedElement.text()).toBe('ID (default)')
    })
  })

  describe('shallowmount', () => {
    beforeEach(async () => {
      const localVue = createLocalVue()

      // Configure the local vue with plugins
      const core = Core.init(localVue).useAll()
      const { router } = core

      await core.configure()

      const options = {
        localVue,
        router
      }

      wrapper = await shallowMount(SortByDropdown, options)
    })

    // it('updates URL when sort option is changed', () => {
    //   // what
    //   const url = wrapper.vm.$route.query

    //   // when
    //   console.log(url)

    //   const expectedQueryParam = 'task_id'
    //   wrapper.vm.sort = expectedQueryParam
    //   // expect
    //   expect(wrapper.vm.$route.query.sort).toBe(expectedQueryParam)
    // })
  })
})
