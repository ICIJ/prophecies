import { createLocalVue, shallowMount } from '@vue/test-utils'
import '@/store'
import Core from '@/core'
import Action from '@/models/Action'
import Task from '@/models/Task'
import Tip from '@/models/Tip'
import User from '@/models/User'
import HistoryListGroup from '@/components/HistoryListGroup'

describe('HistoryListGroup', () => {
  let wrapper

  beforeAll(async () => {
    await Task.api().get()
    await Action.api().get()
    await Tip.api().get()
    await User.api().me()
  })

  beforeEach(async () => {
    const localVue = createLocalVue()
    // Configure the local vue with plugins
    const { store } = Core.init(localVue).useAll()

    wrapper = await shallowMount(HistoryListGroup, {
      localVue,
      store
    })
  })
  it('should display 7 events', () => {
    const elem = wrapper.findAll('history-list-item-stub')
    expect(elem).toHaveLength(7)
  })
  it('should limit view to 5 events', async () => {
    await wrapper.setProps({ limit: 5 })
    const elem = wrapper.findAll('history-list-item-stub')
    expect(elem).toHaveLength(5)
  })
  it('should display the show more button if the limit is inferior to the total number of events', async () => {
    await wrapper.setProps({ limit: 5 })
    let elem = wrapper.find('.history-list-group__see-more')
    expect(elem.exists()).toBeTruthy()

    await wrapper.setProps({ limit: 7 })
    elem = wrapper.find('.history-list-group__see-more')
    expect(elem.exists()).toBeFalsy()
  })

  it('should add 3 more elements to a limited view of 3 events by clicking on See more until they all appear', async () => {
    await wrapper.setProps({ limit: 3 })
    await wrapper.setData({ more: 3 })

    let seeMoreBtn = wrapper.find('.history-list-group__see-more__button')
    seeMoreBtn.trigger('click')
    await wrapper.vm.$nextTick()

    let items = wrapper.findAll('history-list-item-stub')
    expect(items).toHaveLength(6)

    seeMoreBtn = wrapper.find('.history-list-group__see-more__button')
    expect(seeMoreBtn.exists()).toBeTruthy()

    seeMoreBtn.trigger('click')
    await wrapper.vm.$nextTick()

    items = wrapper.findAll('history-list-item-stub')
    expect(items).toHaveLength(7)
    seeMoreBtn = wrapper.find('.history-list-group__see-more__button')
    expect(seeMoreBtn.exists()).toBeFalsy()
  })

  it('should display items in reversed chronological order', () => {
    expect(wrapper.vm.timestamp)

    const unorderedItems = [
      { id: 'history-item-1', timestamp: '2021-10-14T15:27:56.323633Z' },
      { id: 'history-item-2', timestamp: '2021-10-14T15:40:56.323633Z' },
      { id: 'history-item-3', timestamp: '2021-10-14T16:04:13.194403Z' },
      { id: 'history-item-4', timestamp: '2021-09-02T12:58:16.113007Z' },
      { id: 'history-item-5', timestamp: '2021-09-02T12:58:16.113007Z' },
      { id: 'history-item-6', timestamp: '2021-09-02T12:58:16.113007Z' },
      { id: 'history-item-7', timestamp: '2021-09-02T12:58:16.113007Z' }
    ]

    expect(wrapper.vm.items.map(i => ({ id: i.id, timestamp: i.timestamp }))).toEqual(unorderedItems)
    const expectedOrder = [
      { id: 'history-item-3', timestamp: '2021-10-14T16:04:13.194403Z' },
      { id: 'history-item-2', timestamp: '2021-10-14T15:40:56.323633Z' },
      { id: 'history-item-1', timestamp: '2021-10-14T15:27:56.323633Z' },
      { id: 'history-item-4', timestamp: '2021-09-02T12:58:16.113007Z' },
      { id: 'history-item-5', timestamp: '2021-09-02T12:58:16.113007Z' },
      { id: 'history-item-6', timestamp: '2021-09-02T12:58:16.113007Z' },
      { id: 'history-item-7', timestamp: '2021-09-02T12:58:16.113007Z' }
    ]
    expect(wrapper.vm.sortedByTimestampItems.map(i => ({ id: i.id, timestamp: i.timestamp }))).toEqual(expectedOrder)

    const items = wrapper.findAll('history-list-item-stub')
    expect(items).toHaveLength(7)
    for (let i = 0; i < items.length; ++i) {
      expect(items.at(i).attributes().id).toEqual(expectedOrder[i].id)
    }
  })
})
