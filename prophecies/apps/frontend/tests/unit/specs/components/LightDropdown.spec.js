import { createLocalVue, mount } from '@vue/test-utils'

import '@/store'
import Core from '@/core'
import Task from '@/models/Task'
import LightDropdown from '@/components/LightDropdown'

describe('LightDropdown', () => {
  let wrapper

  beforeAll(async () => {
    await Task.api().get()
  })

  beforeEach(async () => {
    const localVue = createLocalVue()
    // Configure the local vue with plugins
    const { i18n } = Core.init(localVue).useAll()
    const all_ = { id: '0_all', name: 'All open tasks' }
    const [t1, t2] = Task.query().whereIdIn(['1', '2']).get()
    const items = [all_, t1, t2]
    const propsData = { items, selectedId: all_.id }
    wrapper = mount(LightDropdown, { localVue, propsData, i18n })
  })
  it('should show All open task selected', () => {
    const element = wrapper.find('.light-dropdown__selected')
    expect(element.text()).toEqual('All open tasks')
  })

  it('should have 3 dropdown items', () => {
    const elements = wrapper.findAll('.dropdown-item')
    expect(elements).toHaveLength(3)
    expect(elements.at(0).text()).toBe('All open tasks')
    expect(elements.at(1).text()).toBe('Addresses')
    expect(elements.at(2).text()).toBe('Shops')
  })
  it('should active the item corresponding to the selected element', async () => {
    const element = wrapper.findAll('.dropdown-item.active')
    expect(element).toHaveLength(1)
    expect(element.at(0).text()).toEqual('All open tasks')
    expect(element.at(0).attributes('data-itemid')).toEqual('0_all')
    await wrapper.setProps({ selectedId: '1' })
    const element2 = wrapper.findAll('.dropdown-item.active')
    expect(element2).toHaveLength(1)
    expect(element2.at(0).text()).toEqual('Addresses')
    expect(element2.at(0).attributes('data-itemid')).toEqual('1')
  })
  it('should emit the item id "1" when Addresses option is clicked', async () => {
    const elementclicked = wrapper.find('.dropdown-item[data-itemid="1"]')
    await elementclicked.trigger('click')
    await wrapper.vm.$nextTick()
    expect(wrapper.emitted()['update:selectedId']).toHaveLength(1)
    expect(wrapper.emitted()['update:selectedId'][0]).toEqual(['1'])
  })
  it('should show/hide the dropdown menu on click', async () => {
    const elementClicked = wrapper.find('.light-dropdown__selected')
    expect(wrapper.vm.show).toBe(false)
    const optionhidden = wrapper.find('.light-dropdown__options.show')
    expect(optionhidden.exists()).toBe(false)

    await elementClicked.trigger('click')
    const options = wrapper.find('.light-dropdown__options.show')
    expect(options.exists()).toBe(true)

    await elementClicked.trigger('click')
    const nooptions = wrapper.find('.light-dropdown__options.show')
    expect(nooptions.exists()).toBe(false)
    expect(wrapper.vm.show).toBe(false)
  })
})
