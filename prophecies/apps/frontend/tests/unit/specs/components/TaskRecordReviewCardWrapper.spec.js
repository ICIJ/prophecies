import { createLocalVue, shallowMount } from '@vue/test-utils'

import '@/store'
import Core from '@/core'
import Task from '@/models/Task'
import ChoiceGroup from '@/models/ChoiceGroup'
import TaskRecordReview from '@/models/TaskRecordReview'
import TaskRecordReviewCardWrapper from '@/components/TaskRecordReviewCardWrapper'
import TaskRecordReviewCardForText from '@/components/TaskRecordReviewCardForText'
import TaskRecordReviewCardForMedia from '@/components/TaskRecordReviewCardForMedia'

describe('TaskRecordReviewCardWrapper', () => {
  let wrapper

  function createContainer() {
    const div = document.createElement('div')
    document.body.appendChild(div)
    return div
  }

  beforeEach(async () => {
    await ChoiceGroup.api().get()
    await Task.api().get()
    await TaskRecordReview.api().get()
  })

  describe('a review within a task of template type "TEXT"', () => {
    beforeEach(() => {
      const attachTo = createContainer()
      const localVue = createLocalVue()
      const propsData = { taskRecordReviewId: '36' }
      // Configure the local vue with plugins
      const { i18n, store, wait } = Core.init(localVue).useAll()
      wrapper = shallowMount(TaskRecordReviewCardWrapper, { attachTo, i18n, localVue, propsData, store, wait })
    })

    it('renders a TaskRecordReviewCardForText', () => {
      expect(wrapper.findComponent(TaskRecordReviewCardForText).exists()).toBeTruthy()
      expect(wrapper.findComponent(TaskRecordReviewCardForMedia).exists()).toBeFalsy()
    })
  })

  describe('a review within a task of template type "MEDIA"', () => {
    beforeEach(() => {
      const attachTo = createContainer()
      const localVue = createLocalVue()
      const propsData = { taskRecordReviewId: '40' }
      // Configure the local vue with plugins
      const { i18n, store, wait } = Core.init(localVue).useAll()
      wrapper = shallowMount(TaskRecordReviewCardWrapper, { attachTo, i18n, localVue, propsData, store, wait })
    })

    it('renders a TaskRecordReviewCardForText', () => {
      expect(wrapper.findComponent(TaskRecordReviewCardForText).exists()).toBeFalsy()
      expect(wrapper.findComponent(TaskRecordReviewCardForMedia).exists()).toBeTruthy()
    })
  })
})
