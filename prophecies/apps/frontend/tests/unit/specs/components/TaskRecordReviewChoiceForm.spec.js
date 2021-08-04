import { createLocalVue, mount } from '@vue/test-utils'
import '@/store'
import Core from '@/core'
import Task from '@/models/Task'
import TaskRecordReview from '@/models/TaskRecordReview'
import ChoiceGroup from '@/models/ChoiceGroup'
import TaskRecordReviewChoiceForm from '@/components/TaskRecordReviewChoiceForm'

describe('TaskRecordReviewChoiceForm', () => {
  let wrapper

  beforeAll(async () => {
    await ChoiceGroup.api().get()
    await Task.api().get()
    await TaskRecordReview.api().get()
  })

  describe('with a pending task record review', () => {
    beforeEach(() => {
      const localVue = createLocalVue()
      const propsData = { taskRecordReviewId: '36' }
      // Configure the local vue with plugins
      Core.init(localVue).useAll()
      wrapper = mount(TaskRecordReviewChoiceForm, { localVue, propsData })
    })

    it('should show 3 choices items', () => {
      const elements = wrapper.findAll('.task-record-review-choice-form__choices__item')
      expect(elements).toHaveLength(3)
    })

    it('should not be in selected state', () => {
      expect(wrapper.classes('task-record-review-choice-form--has-choice')).toBeFalsy()
    })
  })

  describe('with a pending task record review', () => {
    beforeEach(() => {
      const localVue = createLocalVue()
      const propsData = { taskRecordReviewId: '37' }
      // Configure the local vue with plugins
      Core.init(localVue).useAll()
      wrapper = mount(TaskRecordReviewChoiceForm, { localVue, propsData })
    })

    it('should be in selected state', async () => {
      expect(wrapper.classes('task-record-review-choice-form--has-choice')).toBeTruthy()
    })
  })
})
