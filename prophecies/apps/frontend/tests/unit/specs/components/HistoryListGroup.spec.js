import { createLocalVue, shallowMount } from '@vue/test-utils'
import '@/store'
import Core from '@/core'
import Action from '@/models/Action'
import Task from '@/models/Task'
import Tip from '@/models/Tip'
import User from '@/models/User'
import ActionAggregate from '@/models/ActionAggregate'
import HistoryListGroup from '@/components/HistoryListGroup'

describe('HistoryListGroup', () => {
  let wrapper

  beforeAll(async () => {
    await Task.api().get()
    await Action.api().get()
    await ActionAggregate.api().get()
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
  it('should display 10 events', () => {
    const elem = wrapper.findAll('history-list-item-stub')
    expect(elem).toHaveLength(10)
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

    await wrapper.setProps({ limit: 10 })
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
    seeMoreBtn.trigger('click')
    await wrapper.vm.$nextTick()

    items = wrapper.findAll('history-list-item-stub')
    expect(items).toHaveLength(10)
    seeMoreBtn = wrapper.find('.history-list-group__see-more__button')
    expect(seeMoreBtn.exists()).toBeFalsy()
  })

  it('should display items in reversed chronological order', () => {
    const unorderedItems = wrapper.vm.items
    const expectedOrder = wrapper.vm.sortedByTimestampItems
    expect(unorderedItems.sort(wrapper.vm.sortByTimestamp)).toEqual(expectedOrder)

    const items = wrapper.findAll('history-list-item-stub')
    expect(items).toHaveLength(10)
    for (let i = 0; i < items.length; ++i) {
      expect(items.at(i).attributes().id).toEqual(expectedOrder[i].id)
    }
  })

  it('should display the number of checked reviews (subtraction of cancelled from reviewed) grouped by date, by user and by task', () => {
    expect(wrapper.vm.reviewedOrCancelledItems.length).toEqual(4)

    const reviews = wrapper.vm.reviewedItems
    expect(reviews.length).toEqual(3)
    expect(reviews[0].content).toEqual(3) // 3 reviewed 0 cancelled
    expect(reviews[1].content).toEqual(9) // 9 reviewed 0 cancelled
    expect(reviews[2].content).toEqual(53) // 87 reviewed - 34 cancelled
  })
})
