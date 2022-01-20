import { createLocalVue, mount } from '@vue/test-utils'
import '@/store'
import Core from '@/core'
import Action from '@/models/Action'
import TaskRecordChanges from '@/components/TaskRecordChanges'

describe('TaskRecordChanges', () => {
  function createContainer () {
    const div = document.createElement('div')
    document.body.appendChild(div)
    return div
  }

  describe('with zero changes', () => {
    let wrapper

    beforeEach(() => {
      const localVue = createLocalVue()
      const propsData = { actionIds: [] }
      // Configure the local vue with plugins
      const { i18n, store, router, wait } = Core.init(localVue).useAll()
      wrapper = mount(TaskRecordChanges, { localVue, propsData, i18n, store, router, wait })
    })

    it('should show no chnages message', () => {
      const message = wrapper.find('.task-record-review-changes__actions__item--empty')
      expect(message.exists()).toBeTruthy()
    })
  })

  describe('with one change', () => {
    let wrapper

    beforeAll(async () => {
      await Action.api().forTaskRecord(3)
    })

    afterAll(() => {
      Action.deleteAll()
    })

    beforeEach(() => {
      const attachTo = createContainer()
      const localVue = createLocalVue()
      const propsData = { actionIds: ['13'] }
      // Configure the local vue with plugins
      const { i18n, store, wait } = Core.init(localVue).useAll()
      wrapper = mount(TaskRecordChanges, { attachTo, localVue, propsData, i18n, store, wait })
    })

    it('should NOT show no chnages message', () => {
      const message = wrapper.find('.task-record-review-changes__actions__item--empty')
      expect(message.exists()).toBeFalsy()
    })

    it('should show the correct content', () => {
      const action = wrapper.find('.task-record-review-changes__actions__item__content')
      expect(action.text()).toBe('Django classified the record as "Correct"')
    })

    it('should show one action', () => {
      const actions = wrapper.findAll('.task-record-review-changes__actions')
      expect(actions).toHaveLength(1)
    })
  })
})
