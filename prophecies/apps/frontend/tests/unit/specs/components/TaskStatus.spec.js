import { createLocalVue, mount } from '@vue/test-utils'
import TaskStatus from '@/components/TaskStatus'
import Task from '@/models/Task'
import Core from '@/core'

describe('TaskStatus', () => {
  let wrapper

  beforeAll(() => {
    Task.insert({
      data: { id: '1000', name: 'foo', status: 'OPEN' }
    })
  })

  beforeEach(async () => {
    const localVue = createLocalVue()
    // Configure the local vue
    const core = Core.init(localVue).useI18n()
    // Load the settings
    await core.configure()
    // Those core properties must be available for each test
    const { i18n, store } = core
    const propsData = { taskId: '1000' }
    wrapper = mount(TaskStatus, { i18n, store, localVue, propsData })
  })

  describe('with an open task', () => {
    beforeEach(() => {
      // Ensure the task is open by default
      Task.update({
        where: '1000',
        data: {
          status: 'OPEN'
        }
      })
    })

    it('should show "Open" as a label', () => {
      expect(wrapper.text()).toBe('Open')
    })

    it('should use "CheckIcon" as icon', () => {
      expect(wrapper.vm.icon).toBe('CheckIcon')
    })

    it('should use the "task-status--open" class', () => {
      expect(wrapper.classes('task-status--open')).toBeTruthy()
    })
  })

  describe('with a locked task', () => {
    beforeEach(() => {
      // Ensure the task is open by default
      Task.update({
        where: '1000',
        data: {
          status: 'LOCKED'
        }
      })
    })

    it('should show "Locked" as a label', () => {
      expect(wrapper.text()).toBe('Locked')
    })

    it('should use "LockIcon" as icon', () => {
      expect(wrapper.vm.icon).toBe('LockIcon')
    })

    it('should use the "task-status--locked" class', () => {
      expect(wrapper.classes('task-status--locked')).toBeTruthy()
    })
  })

  describe('with a closed task', () => {
    beforeEach(() => {
      // Ensure the task is open by default
      Task.update({
        where: '1000',
        data: {
          status: 'CLOSED'
        }
      })
    })

    it('should show "Closed" as a label', () => {
      expect(wrapper.text()).toBe('Closed')
    })

    it('should use no icon', () => {
      expect(wrapper.vm.icon).toBeFalsy()
    })

    it('should use the "task-status--closed" class', () => {
      expect(wrapper.classes('task-status--closed')).toBeTruthy()
    })
  })
})
