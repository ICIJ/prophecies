import { createLocalVue, shallowMount } from '@vue/test-utils'

import '@/store'
import Core from '@/core'
import TaskRecord from '@/models/TaskRecord'
import TaskRecordMedia from '@/models/TaskRecordMedia'

import TaskRecordMediaView from '@/components/TaskRecordMediaView'

jest.mock('lodash', () => ({
  ...jest.requireActual('lodash'),
  uniqueId: jest.fn().mockReturnValue('unique-id')
}))

describe('TaskRecordMediaView', () => {

  beforeEach(async () => {
    await TaskRecord.api().get()
    await TaskRecordMedia.api().get()
  })

  describe('a media without expand button', () => {
    let wrapper

    beforeEach(() => {
      const localVue = createLocalVue()
      const { store } = Core.init(localVue).useAll()
      const propsData = { taskRecordMediaId: 0, expand: false }
      wrapper = shallowMount(TaskRecordMediaView, { localVue, store, propsData })
    })

    it('initializes with correct elements', () => {
      expect(wrapper.vm.taskRecordMedia).toBeTruthy()
      expect(wrapper.vm.modalId).toBe('unique-id')
    })

    it('computes isImage correctly', () => {
      expect(wrapper.vm.isImage).toBe(true)
    })

    it('does not prevent default when expand is false', () => {
      const event = { preventDefault: jest.fn() }
      wrapper.vm.mightPrevent(event)
      expect(event.preventDefault).not.toHaveBeenCalled()
    })
  })

  describe('a media with expand button', () => {
    let wrapper

    beforeEach(() => {
      const localVue = createLocalVue()
      const { store } = Core.init(localVue).useAll()
      const propsData = { taskRecordMediaId: 0, expand: true }
      wrapper = shallowMount(TaskRecordMediaView, { localVue, store, propsData })
    })

    it('calls mightPrevent and prevents default when expand is true', () => {
      const event = { preventDefault: jest.fn() }
      wrapper.vm.mightPrevent(event)
      expect(event.preventDefault).toHaveBeenCalled()
    })
  })
})
