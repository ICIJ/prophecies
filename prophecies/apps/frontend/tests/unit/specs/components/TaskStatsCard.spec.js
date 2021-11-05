import { createLocalVue, shallowMount } from '@vue/test-utils'

import '@/store'
import Core from '@/core'
import Task from '@/models/Task'
import TaskStatsCard from '@/components/TaskStatsCard'

describe('TaskStatsCard', () => {
  let wrapper

  beforeAll(async () => {
    await Task.api().get()
  })

  beforeEach(() => {
    const localVue = createLocalVue()
    // Configure the local vue with plugins
    const { i18n } = Core.init(localVue).useAll()
    const propsData = { taskId: '1', team: false }
    wrapper = shallowMount(TaskStatsCard, { localVue, propsData, i18n })
  })

  it('should show the user progress', () => {
    const element = wrapper.find('.task-stats-card__progress')
    expect(element.text()).toBe('50%')
  })

  it('should show the team progress', async () => {
    await wrapper.setProps({ team: true })
    const element = wrapper.find('.task-stats-card__progress')
    expect(element.text()).toBe('40%')
  })

  it('should show 3 rounds', () => {
    const elements = wrapper.findAll('.task-stats-card__progress-by-round__item')
    expect(elements).toHaveLength(3)
  })

  it('should show 100% progress at round 1 for the user', () => {
    const element = wrapper.findAll('.task-stats-card__progress-by-round__item__value').at(0)
    expect(element.text()).toBe('100%')
  })

  it('should show 50% progress at round 1 for the team', async () => {
    await wrapper.setProps({ team: true })
    const element = wrapper.findAll('.task-stats-card__progress-by-round__item__value').at(0)
    expect(element.text()).toBe('50%')
  })

  it('should show 25% progress at round 2 for the user', () => {
    const element = wrapper.findAll('.task-stats-card__progress-by-round__item__value').at(1)
    expect(element.text()).toBe('25%')
  })

  it('should show 25% progress at round 2 for the team', async () => {
    await wrapper.setProps({ team: true })
    const element = wrapper.findAll('.task-stats-card__progress-by-round__item__value').at(1)
    expect(element.text()).toBe('25%')
  })

  it('should show 25% progress at round 3 for the user', () => {
    const element = wrapper.findAll('.task-stats-card__progress-by-round__item__value').at(2)
    expect(element.text()).toBe('25%')
  })

  it('should show 30% progress at round 3 for the team', async () => {
    await wrapper.setProps({ team: true })
    const element = wrapper.findAll('.task-stats-card__progress-by-round__item__value').at(2)
    expect(element.text()).toBe('30%')
  })
  it('should show the task locked', async () => {
    const element = wrapper.find('.task-stats-card__status__lock--locked')
    expect(element.exists()).toBe(true)
  })

  describe('Extended task stats card', () => {
    it('should display the read tips button', async () => {
      await wrapper.setProps({ extended: true })
      const readTipsButton = wrapper.find('.task-stats-card__read-tips')
      expect(readTipsButton.exists()).toBeTruthy()
    })
  })
})
