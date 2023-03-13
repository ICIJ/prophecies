import {createLocalVue, mount} from '@vue/test-utils'
import TaskListItem from '@/components/TaskListItem'
import Task from '@/models/Task'
import Core from '@/core'

describe('TaskListItem', () => {

  beforeAll(async () => {
    await Task.api().get()
  })

  describe('task list item with a project and a status', () => {
    let wrapper

    beforeEach(async () => {
      const localVue = createLocalVue()
      const propsData = {taskId: '1'}
      // Configure the local vue
      const core = Core.init(localVue).useAll()
      // Configure the core
      await core.configure()
      // Get router from core
      const {i18n, store, router} = core
      // Finally, instanciate the component
      wrapper = mount(TaskListItem, {localVue, propsData, i18n, store, router})
    })

    it('should show the link by default', () => {
      expect(wrapper.find('.task-list-item__link').text()).toBe('Addresses')
    })

    it('should show the project by default', () => {
      expect(wrapper.find('.task-list-item__project').text()).toBe('in Chronos')
    })

    it('should show the status by default', () => {
      expect(wrapper.find('.task-list-item__status').text()).toBe('Locked')
    })
  })

  describe('task list item without project nor a status', () => {
    let wrapper

    beforeEach(async () => {
      const localVue = createLocalVue()
      const propsData = {taskId: '1', noStatus: true, noProject: true}
      // Configure the local vue
      const core = Core.init(localVue).useAll()
      // Configure the core
      await core.configure()
      // Get router from core
      const {i18n, store, router} = core
      // Finally, instanciate the component
      wrapper = mount(TaskListItem, {localVue, propsData, i18n, store, router})
    })

    it('should show the name by default', () => {
      expect(wrapper.find('.task-list-item__link').text()).toBe('Addresses')
    })

    it('should not show the project', () => {
      expect(wrapper.find('.task-list-item__project').exists()).toBeFalsy()
    })

    it('should not show the status', () => {
      expect(wrapper.find('.task-list-item__status').exists()).toBeFalsy()
    })
  })

  describe('disabled task list item with an unknown task', () => {
    let wrapper

    beforeEach(async () => {
      const localVue = createLocalVue()
      const propsData = {taskId: '404'}
      // Configure the local vue
      const core = Core.init(localVue).useAll()
      // Configure the core
      await core.configure()
      // Get router from core
      const {i18n, store, router} = core
      // Finally, instanciate the component
      wrapper = mount(TaskListItem, {localVue, propsData, i18n, store, router})
    })

    it('should show nothing when the task is unknown', () => {
      const text = wrapper.text()
      expect(text).toBe('')
    })
  })
})
