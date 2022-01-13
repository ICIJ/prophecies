import { createLocalVue, mount, shallowMount } from '@vue/test-utils'
import '@/store'
import Core from '@/core'
import Task from '@/models/Task'
import TaskRecord from '@/models/TaskRecord'
import TaskRecordReview from '@/models/TaskRecordReview'
import ChoiceGroup from '@/models/ChoiceGroup'
import TaskRecordReviewChoiceForm from '@/components/TaskRecordReviewChoiceForm'

describe('TaskRecordReviewChoiceForm', () => {
  let wrapper

  function createContainer() {
    const div = document.createElement('div')
    document.body.appendChild(div)
    return div
  }

  beforeAll(async () => {
    await ChoiceGroup.api().get()
    await Task.api().get()
    await TaskRecordReview.api().get()
  })

  describe('with a pending task record review', () => {
    beforeEach(() => {
      const attachTo = createContainer()
      const localVue = createLocalVue()
      const propsData = { taskRecordReviewId: '36' }
      // Configure the local vue with plugins
      const { store, wait } = Core.init(localVue).useAll()
      wrapper = mount(TaskRecordReviewChoiceForm, { attachTo, localVue, propsData, store, wait })
    })

    it('should show 3 choices items', () => {
      const elements = wrapper.findAll('.choice-group-buttons__item')
      expect(elements).toHaveLength(3)
    })

    it('should not be in selected state', () => {
      const element = wrapper.find('.task-record-review-choice-form')
      expect(element.classes('task-record-review-choice-form--has-choice')).toBeFalsy()
    })

    it('should emit a "submit" event when click on the first button', async () => {
      const firstBtn = wrapper.findAll('.choice-group-buttons__item__button').at(0)
      firstBtn.trigger('click')
      await wrapper.vm.$nextTick()
      expect(wrapper.emitted().submit).toHaveLength(1)
    })

    it('should not emit a "submit" event when click on the second button', async () => {
      const secondBtn = wrapper.findAll('.choice-group-buttons__item__button').at(1)
      secondBtn.trigger('click')
      await wrapper.vm.$nextTick()
      expect(wrapper.emitted().submit).toBeUndefined()
    })

    it('should focus on the alternative value input when click on the second button', async () => {
      const secondBtn = wrapper.findAll('.choice-group-buttons__item__button').at(1)
      const input = wrapper.find(wrapper.vm.alternativeValueInputSelector)
      secondBtn.trigger('click')
      await wrapper.vm.$nextTick()
      expect(input.element).toBe(document.activeElement)
    })
  })

  describe('with a done task record review', () => {
    beforeEach(() => {
      const localVue = createLocalVue()
      const propsData = { taskRecordReviewId: '37' }
      // Configure the local vue with plugins
      const { store, wait } = Core.init(localVue).useAll()
      wrapper = mount(TaskRecordReviewChoiceForm, { localVue, propsData, store, wait })
    })

    it('should be in selected state', async () => {
      const element = wrapper.find('.task-record-review-choice-form')
      expect(element.classes('task-record-review-choice-form--has-choice')).toBeTruthy()
    })
  })

  describe('with a task status', () => {
    beforeEach(() => {
      const localVue = createLocalVue()
      const propsData = { taskRecordReviewId: '25' }
      // Configure the local vue with plugins
      const { store, wait } = Core.init(localVue).useAll()
      wrapper = shallowMount(TaskRecordReviewChoiceForm, { localVue, propsData, store, wait })
    })

    it('should be in enabled state when record is not locked and task is open ', () => {
      const element = wrapper.find('.task-record-review-choice-form')
      expect(element.classes('task-record-review-choice-form--is-locked')).toBeFalsy()
    })

    it('should be in disabled state when record is locked and task is open ', async () => {
      const { taskId, taskRecordId } = TaskRecordReview.find('38')
      Task.update({ where: taskId, data: { status: 'OPEN' } })
      TaskRecord.update({ where: taskRecordId, data: { locked: true } })

      const propsData = { taskRecordReviewId: '38' }
      await wrapper.setProps(propsData)
      const element = wrapper.find('.task-record-review-choice-form')
      expect(element.classes('task-record-review-choice-form--is-locked')).toBeTruthy()
    })

    it('should be in disabled state when record is locked and task is locked', async () => {
      const { taskId, taskRecordId } = TaskRecordReview.find('38')
      Task.update({ where: taskId, data: { status: 'LOCKED' } })
      TaskRecord.update({ where: taskRecordId, data: { locked: true } })

      const propsData = { taskRecordReviewId: '38' }
      await wrapper.setProps(propsData)
      const element = wrapper.find('.task-record-review-choice-form')
      expect(element.classes('task-record-review-choice-form--is-locked')).toBeTruthy()
    })    
    
    it('should not be in disabled state when record is not locked and task is open', async () => {
      const { taskId, taskRecordId } = TaskRecordReview.find('38')
      Task.update({ where: taskId, data: { status: 'OPEN' } })
      TaskRecord.update({ where: taskRecordId, data: { locked: false } })

      const propsData = { taskRecordReviewId: '38' }
      await wrapper.setProps(propsData)
      const element = wrapper.find('.task-record-review-choice-form')
      expect(element.classes('task-record-review-choice-form--is-locked')).toBeFalsy()
    })
  })

})