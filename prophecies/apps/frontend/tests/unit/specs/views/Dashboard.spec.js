import {createLocalVue, shallowMount} from '@vue/test-utils'

import '@/store'
import Core from '@/core'
import Task from '@/models/Task'
import Dashboard from '@/views/Dashboard'

describe('Dashboard', () => {
  let wrapper

  beforeAll(async () => {
    await Task.api().get()
  })

  beforeEach(async () => {
    const localVue = createLocalVue()
    // Configure the local vue with plugins
    const {i18n, wait, store} = Core.init(localVue).useAll()

    wrapper = await shallowMount(Dashboard, {
      i18n,
      localVue,
      store,
      wait
    })
  })

  afterEach(async () => {
    // Prevent a Vue warning in the next tick when the parentNode doesnt exist:
    // > TypeError: Cannot read property 'createElement' of null
    // @see https://stackoverflow.com/a/62262333
    wrapper.destroy()
  })

  it('should sort the task by priority and name without the closed ones', () => {
    expect(wrapper.vm.tasks).toHaveLength(3)
    expect(wrapper.vm.tasks[0].id).toBe('1')
    expect(wrapper.vm.tasks[1].id).toBe('2')
    expect(wrapper.vm.tasks[2].id).toBe('4')
  })

  it('should not display tasks with no task record or closed tasks', async () => {
    expect(wrapper.vm.tasks).toHaveLength(3)
    const element = wrapper.findAll('task-stats-card-stub')
    expect(element).toHaveLength(3)
  })

  it('should show the link to the stats', () => {
    const element = wrapper.find('.dashboard__container__left-panel__stats-link')
    expect(element.text()).toBe('All my tasks')
  })
})
