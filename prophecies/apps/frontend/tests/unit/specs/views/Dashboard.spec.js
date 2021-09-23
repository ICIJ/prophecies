import { createLocalVue, mount, shallowMount } from '@vue/test-utils'

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
    const { wait, store } =Core.init(localVue).useAll()

    wrapper = await shallowMount(Dashboard, {
        localVue,
        store,
        wait,
      })
  })

  it('should sort the task with the closed ones at the end', () => {
      expect(wrapper.vm.tasks).toHaveLength(4)
      expect(wrapper.vm.tasks[3].status).toEqual("CLOSED")
      const element = wrapper.findAll("task-stats-card-stub")
      expect(element).toHaveLength(4)
      expect(element.at(3).attributes().taskid).toEqual('3')
  })

})
