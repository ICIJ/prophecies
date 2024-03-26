import { createLocalVue, shallowMount } from '@vue/test-utils'

import '@/store'
import Core from '@/core'
import Task from '@/models/Task'
import User from '@/models/User'
import UserTaskStatsCard from '@/components/UserTaskStatsCard'

describe('UserTaskStatsCard', () => {
  let wrapper

  beforeAll(async () => {
    await User.api().get()
    await Task.api().get()
  })

  beforeEach(async () => {
    const localVue = createLocalVue()
    // Configure the local vue with plugins
    const { i18n } = Core.init(localVue).useAll()
    const propsData = { taskIds: ['1', '3'], userId: 'django' }
    wrapper = shallowMount(UserTaskStatsCard, { localVue, propsData, i18n })

    await wrapper.vm.setup()
  })
  it('should show the progress of all open task', async () => {
    const element = wrapper.find('task-stats-card-all-rounds-stub')
    const { progress, done, pending } = element.attributes()
    expect(Number(done)).toBe(15)
    expect(Number(pending)).toBe(290)
    expect(Number(progress)).toBeCloseTo(11.76, 1)
  })

  it('should show the dropdown menu with "All open task" selected by default ', () => {
    const element = wrapper.find('.user-task-stats-card__dropdown')
    expect(element.attributes('selectedid')).toBe('0_all')
  })

  it('should set the selected option Addresses active', async () => {
    await wrapper.setData({ selectedTaskId: '1' })

    const selected = wrapper.find('.user-task-stats-card__dropdown')
    expect(selected.attributes('selectedid')).toBe('1')

    const allrounds = wrapper.find('task-stats-card-all-rounds-stub')
    const { progress, done, pending } = allrounds.attributes()
    expect(Number(done)).toBe(7)
    expect(Number(pending)).toBe(98)
    expect(Number(progress)).toBeCloseTo(6.66, 1)
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

  it('has the title all records', () => {
    expect(wrapper.text()).toContain('All records')
  })

  describe('User stats of user with no open task', () => {
    beforeEach(() => {
      Task.update({ where: '3', data: { status: 'CLOSED' } })
      Task.update({ where: '1', data: { status: 'CLOSED' } })
      const localVue = createLocalVue()
      // Configure the local vue with plugins
      const { i18n } = Core.init(localVue).useAll()
      const propsData = { taskIds: ['1', '3'], userId: 'django' }
      wrapper = shallowMount(UserTaskStatsCard, { localVue, propsData, i18n })
    })
    it('should show 0 as progress for all open task dropdown item', async () => {
      const element = wrapper.find('task-stats-card-all-rounds-stub')
      const { progress, done, pending } = element.attributes()
      expect(Number(done)).toBe(0)
      expect(Number(pending)).toBe(0)
      expect(Number(progress)).toBeCloseTo(0)
    })
  })
})
