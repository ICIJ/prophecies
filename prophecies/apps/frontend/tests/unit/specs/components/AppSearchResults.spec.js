import { createLocalVue, shallowMount } from '@vue/test-utils'
import { BTab } from 'bootstrap-vue'
import AppSearchResults from '@/components/AppSearchResults'
import Core from '@/core'
import Task from '@/models/Task'
import TaskRecordReview from '@/models/TaskRecordReview'
import Tip from '@/models/Tip'

describe('AppSearchResults', () => {
  describe('with 2 tasks', () => {
    let wrapper

    beforeAll(async () => {
      await Task.api().get()
      await TaskRecordReview.api().get()
      await Tip.api().get()
    })

    beforeEach(async () => {
      const localVue = createLocalVue()
      const core = Core.init(localVue).useAll()
      const { i18n, store, wait } = core
      const stubs = ['router-link']
      await core.configure()
      const propsData = {
        query: 'test',
        queryset: [
          { id: '38', type: 'TaskRecordReview', querysetId: 'qs-1' },
          { id: '37', type: 'TaskRecordReview', querysetId: 'qs-1' },
          { id: '36', type: 'TaskRecordReview', querysetId: 'qs-1' },
          { id: '4', type: 'Tip', querysetId: 'qs-2' }
        ],
        counts: [
          { count: 3, querysetId: 'qs-1' },
          { count: 1, querysetId: 'qs-2' }
        ]
      }
      // Finally, instantiate the component
      wrapper = shallowMount(AppSearchResults, { i18n, localVue, propsData, stubs, store, wait })
    })

    it('should have 4 tabs', () => {
      expect(wrapper.findAllComponents(BTab)).toHaveLength(4)
    })

    it('should have 3 items for task 1', () => {
      expect(wrapper.vm.querysetTaskRecordReviews('1')).toHaveLength(3)
    })

    it('should have 2 items for task 1', async () => {
      await wrapper.setProps({
        queryset: [
          { id: '37', type: 'TaskRecordReview', querysetId: 'qs-1' },
          { id: '36', type: 'TaskRecordReview', querysetId: 'qs-1' }
        ]
      })
      expect(wrapper.vm.querysetTaskRecordReviews('1')).toHaveLength(2)
    })

    it('should have 1 tip', () => {
      expect(wrapper.vm.querysetTips()).toHaveLength(1)
    })

    it('should count 3 reviews for task 1', () => {
      expect(wrapper.vm.taskRecordReviewsCount('1')).toEqual(3)
    })

    it('should count 0 reviews for task 2', () => {
      expect(wrapper.vm.taskRecordReviewsCount('2')).toEqual(0)
    })

    it('should count 1 tip', async () => {
      expect(wrapper.vm.tipCount()).toEqual(1)
    })
  })
})
