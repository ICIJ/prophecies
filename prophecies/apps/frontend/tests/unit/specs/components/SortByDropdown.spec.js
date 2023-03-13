import {createLocalVue, mount} from '@vue/test-utils'
import Core from '@/core'
import SortByDropdown from '@/components/SortByDropdown'

describe('SortByDropdown', () => {
  let wrapper

  beforeEach(async () => {
    const localVue = createLocalVue()

    // Configure the local vue with plugins
    const core = Core.init(localVue).useAll()
    const {router, i18n} = core

    const propsData = {
      sort: 'task_id',
      options: [
        {value: 'task_id', label: 'ID (default)', $isDefault: true}
      ]
    }

    await core.configure()

    const options = {
      i18n,
      localVue,
      propsData,
      router
    }

    wrapper = await mount(SortByDropdown, options)
  })

  it('selects the ID as the default sorting value', () => {
    const selectedElement = wrapper.find('.multiselect__single')
    expect(selectedElement.text()).toBe('ID (default)')
  })
  // it('updates URL when sort option is changed', () => {
  //   // what
  //   const url = wrapper.vm.$route.query
  //   // when
  //   console.log(url)

  //   const expectedQueryParam = 'task_id'
  //   wrapper.vm.intermediarySort = expectedQueryParam
  //   // expect
  //   expect(wrapper.vm.$route.query.sort).toBe(expectedQueryParam)
  // })
})
