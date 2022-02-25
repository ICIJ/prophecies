import { createLocalVue, shallowMount } from '@vue/test-utils'

import '@/store'
import Core from '@/core'
import Task from '@/models/Task'
import User from '@/models/User'
import UserTaskStatsCard from '@/components/UserTaskStatsCard'

describe('TaskStatsCard', () => {
  let wrapper

  beforeAll(async () => {
    await User.api().get()
    await Task.api().get()
  })

  beforeEach(async () => {
    const localVue = createLocalVue()
    // Configure the local vue with plugins
    const { i18n } = Core.init(localVue).useAll()
    const propsData = { taskIds: ['1', '2'], userId: 'django' }
    wrapper = shallowMount(UserTaskStatsCard, { localVue, propsData, i18n })

    await wrapper.vm.setup()
  })
  it('should show the progress of all open task', async () => {
    const element = wrapper.find('task-stats-card-all-rounds-stub')
    const { progress, done, pending } = element.attributes()
    expect(Number(done)).toBe(7)
    expect(Number(pending)).toBe(98)
    expect(Number(progress)).toBeCloseTo(3.33, 1)
  })

  it('should set the selected option Addresses active', async () => {
    await wrapper.setData({ selectedTaskId: '1' })

    const selected = wrapper.find('.user-task-stats-card__dropdown__selected')
    expect(selected.text()).toBe('Addresses')
    const element = wrapper.find('.dropdown-item.active')
    expect(element.text()).toBe('Addresses')

    const allrounds = wrapper.find('task-stats-card-all-rounds-stub')
    const { progress, done, pending } = allrounds.attributes()
    expect(Number(done)).toBe(7)
    expect(Number(pending)).toBe(98)
    expect(Number(progress)).toBeCloseTo(6.66, 1)
  })
  it('should show the dropdown menu with "All open task" selected', () => {
    const element = wrapper.find('.user-task-stats-card__dropdown')
    expect(element.exists()).toBeTruthy()
    const selected = wrapper.find('.user-task-stats-card__dropdown__selected')
    expect(selected.text()).toBe('All open tasks')
    const activeOption = wrapper.find('.dropdown-item.active')
    expect(activeOption.text()).toBe('All open tasks')
  })

  it('should show 3 dropdown options', () => {
    const elements = wrapper.findAll('.dropdown-item')
    expect(elements).toHaveLength(3)
    expect(elements.at(0).text()).toBe('All open tasks')
    expect(elements.at(1).text()).toBe('Addresses')
    expect(elements.at(2).text()).toBe('Shops')
  })

  it('retrieves stats for a user with no stats', () => {
    const avg = wrapper.vm.getAverage([])
    expect(avg.done).toEqual(0)
    expect(avg.pending).toEqual(0)
    expect(avg.progress).toEqual(0)
  })

  it('has the title all records', () => {
    expect(wrapper.text()).toContain('All records')
  })
})
