import { createLocalVue, mount } from '@vue/test-utils'
import TaskLink from '@/components/TaskLink'
import Task from '@/models/Task'
import Core from '@/core'

describe('TaskLink', () => {

  beforeAll(async () => {
    await Task.api().get()
  })

  describe('task link without slot', () => {
    let wrapper

    beforeEach(async () => {
      const localVue = createLocalVue()
      const propsData = { taskId: '1', noStatus: true }
      // Configure the local vue
      const core = Core.init(localVue).useAll()
      // Configure the core
      await core.configure()
      // Get router from core
      const { i18n, store, router } = core
      // Finally, instanciate the component
      wrapper = mount(TaskLink, { localVue, propsData, i18n, store, router })
    })

    it('should build a link to the user profile', () => {
      const href = wrapper.attributes('href')
      expect(href).toBe('#/task-record-reviews/1')
    })

    it('should show the name by default', () => {
      const text = wrapper.text()
      expect(text).toBe('Addresses')
    })
  })

  describe('task link with slot', () => {
    let wrapper

    beforeEach(async () => {
      const localVue = createLocalVue()
      const propsData = { taskId: '1' }
      // Configure the local vue
      const core = Core.init(localVue).useAll()
      // Configure the core
      await core.configure()
      // Get router from core
      const { i18n, store, router } = core
      const scopedSlots = { default: '<template slot-scope="{ task }">{{ task.name }} task in {{ task.project.name }}</template>' }
      // Finally, instanciate the component
      wrapper = mount(TaskLink, { localVue, propsData, i18n, store, router, scopedSlots })
    })

    it('should show the email instead of the username', () => {
      const text = wrapper.text()
      expect(text).toBe('Addresses task in Chronos')
    })
  })

  describe('disabled task link with an unknown task', () => {
    let wrapper

    beforeEach(async () => {
      const localVue = createLocalVue()
      const propsData = { taskId: '404' }
      // Configure the local vue
      const core = Core.init(localVue).useAll()
      // Configure the core
      await core.configure()
      // Get router from core
      const { i18n, store, router } = core
      // Finally, instanciate the component
      wrapper = mount(TaskLink, { localVue, propsData, i18n, store, router })
    })

    it('should show nothing when the task is unknown', () => {
      const text = wrapper.text()
      expect(text).toBe('')
    })
  })
})
