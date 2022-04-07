import { createLocalVue, shallowMount } from '@vue/test-utils'

import '@/store'
import Core from '@/core'
import Task from '@/models/Task'
import TaskUserStatistics from '@/models/TaskUserStatistics'
import User from '@/models/User'
import TaskStatsCard from '@/components/TaskStatsCard'

describe('TaskStatsCard', () => {
  let wrapper
  beforeAll(async () => {
    await Task.api().get()
    await TaskUserStatistics.api().get()
  })
  describe('Progress of specific checker id (1)', () => {
    beforeEach(async () => {
      const localVue = createLocalVue()
      // Configure the local vue with plugins
      const { i18n } = Core.init(localVue).useAll()
      const propsData = { taskId: '1', checkerId: '1' }
      wrapper = shallowMount(TaskStatsCard, { localVue, propsData, i18n })
    })
    it('should show 3 rounds', () => {
      const elements = wrapper.findAll('stats-by-round-stub')
      expect(elements).toHaveLength(3)
    })
    it('should show 6% progress at round 1 for the user  ', () => {
      const element = wrapper.findAll('stats-by-round-stub').at(0)
      const progressString = element.attributes('progress')
      expect(Number(progressString)).toBeCloseTo(6, 0)
    })
    it('should show 0 progress at round 2 for the user  ', () => {
      const element = wrapper.findAll('stats-by-round-stub').at(1)
      const progressString = element.attributes('progress')
      expect(progressString).toBe('0')
    })
    it('should show  0 progress at round 3 for the user  ', () => {
      const element = wrapper.findAll('stats-by-round-stub').at(2)
      const progressString = element.attributes('progress')
      expect(progressString).toBe('0')
    })
  })

  describe('Progress of team and connected user (me)', () => {
    beforeAll(async () => {
      await Task.api().get()
      await User.api().me()
    })

    beforeEach(() => {
      const localVue = createLocalVue()
      // Configure the local vue with plugins
      const { i18n } = Core.init(localVue).useAll()
      const propsData = { taskId: '1', team: false }
      wrapper = shallowMount(TaskStatsCard, { localVue, propsData, i18n })
    })

    afterAll(async () => {
      wrapper.destroy()
    })
    it('should show the team progress', async () => {
      await wrapper.setProps({ team: true })
      const element = wrapper.find('task-progress-stub')
      expect(element.attributes('progress')).toBe('40')
    })

    it('should show 3 rounds', () => {
      const elements = wrapper.findAll('stats-by-round-stub')
      expect(elements).toHaveLength(3)
    })

    it('should show 100% progress at round 1 for the user', () => {
      const element = wrapper.findAll('stats-by-round-stub').at(0)
      expect(element.attributes('progress')).toBe('100')
    })

    it('should show 50% progress at round 1 for the team', async () => {
      await wrapper.setProps({ team: true })
      const element = wrapper.findAll('stats-by-round-stub').at(0)
      expect(element.attributes('progress')).toBe('50')
    })

    it('should show 25% progress at round 2 for the user', () => {
      const element = wrapper.findAll('stats-by-round-stub').at(1)
      expect(element.attributes('progress')).toBe('25')
    })

    it('should show 25% progress at round 2 for the team', async () => {
      await wrapper.setProps({ team: true })
      const element = wrapper.findAll('stats-by-round-stub').at(1)
      expect(element.attributes('progress')).toBe('25')
    })

    it('should show 25% progress at round 3 for the user', () => {
      const element = wrapper.findAll('stats-by-round-stub').at(2)
      expect(element.attributes('progress')).toBe('25')
    })

    it('should show 30% progress at round 3 for the team', async () => {
      await wrapper.setProps({ team: true })
      const element = wrapper.findAll('stats-by-round-stub').at(2)
      expect(element.attributes('progress')).toBe('30')
    })
  })
})
