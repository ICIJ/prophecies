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
})
