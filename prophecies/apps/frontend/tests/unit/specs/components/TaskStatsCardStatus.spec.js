import { createLocalVue, shallowMount } from '@vue/test-utils'

import '@/store'
import Core from '@/core'
import Task from '@/models/Task'
import TaskStatsCardStatus from '@/components/TaskStatsCardStatus'

describe('Task stats card status', () => {
  let wrapper

  beforeAll(async () => {
    await Task.api().get()
  })
  beforeEach(() => {
    const localVue = createLocalVue()
    // Configure the local vue with plugins
    const { i18n } = Core.init(localVue).useAll()
    const propsData = { taskId: '1', extended: false }
    wrapper = shallowMount(TaskStatsCardStatus, { localVue, propsData, i18n })
  })
  it('should display the read tips button', async () => {
    const readTipsButton = wrapper.find('.task-stats-card__read-tips')
    expect(readTipsButton.exists()).toBeFalsy()
    await wrapper.setProps({ extended: true })
    const readTipsButtonExt = wrapper.find('.task-stats-card__read-tips')
    expect(readTipsButtonExt.exists()).toBeTruthy()
  })

  it('should show the task status', async () => {
    const element = wrapper.find('task-status-stub')
    expect(element.exists()).toBe(true)
  })

  it('should show the task priority color according to the priority level', async () => {
    let element = wrapper.find('.task-stats-card__status__top__priority')
    expect(element.text()).toBe('Priority 1')
    element.classes().includes('bg-priority-top')
    await wrapper.setProps({ taskId: '2', extended: false })
    element = wrapper.find('.task-stats-card__status__top__priority')
    expect(element.text()).toBe('Priority 2')
    element.classes().includes('bg-priority-high')
    await wrapper.setProps({ taskId: '5', extended: false })
    element = wrapper.find('.task-stats-card__status__top__priority')
    expect(element.text()).toBe('Priority 3')
    element.classes().includes('bg-priority-medium')
    await wrapper.setProps({ taskId: '4', extended: false })
    element = wrapper.find('.task-stats-card__status__top__priority')
    expect(element.text()).toBe('Priority 4')
    element.classes().includes('bg-priority-low')
  })
})
