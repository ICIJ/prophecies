import {
  createLocalVue,
  shallowMount
} from '@vue/test-utils'
import Core from '@/core'
import TaskRecordReviewList from '@/views/TaskRecordReviewList'
import Task from '@/models/Task'

describe('TaskRecordReviewList', () => {
  function createContainer() {
    const div = document.createElement('div')
    document.body.appendChild(div)
    return div
  }

  describe('Select record', () => {
    let wrapper
    let options

    beforeEach(async () => {
      const attachTo = createContainer()
      const localVue = createLocalVue()

      // Configure the local vue
      const {i18n, wait, store, router} = await Core.init(localVue).useAll()
      const propsData = {taskId: '1'}
      const stubs = ['router-link', 'app-waiter']
      // Finally, instanciate the component
      options = {
        i18n,
        attachTo,
        localVue,
        propsData,
        router,
        stubs,
        store,
        wait
      }
      wrapper = await shallowMount(TaskRecordReviewList, options)
      await wrapper.vm.setup()
    })

    afterEach(async () => {
      Task.deleteAll()
    })
    describe('Selection on opened task', () => {
      beforeEach(async () => {
        await Task.update({where: '1', data: {status: 'OPEN'}})
      })
      it('should display "Select all records" or "Select 1 record" according to the number of records', async () => {
        await wrapper.setData({
          pagination: {
            count: 0
          },
          selectedIds: {},
          taskRecordReviewIds: ['38']
        })
        let selectAllTextContainer = await wrapper.find('.task-record-review-list__container__select-all')
        expect(selectAllTextContainer.text()).toBe('Select 1 record')
        await wrapper.setData({
          pagination: {
            count: 0
          },
          selectedIds: {},
          taskRecordReviewIds: ['38', '37']
        })
        selectAllTextContainer = await wrapper.find('.task-record-review-list__container__select-all')
        expect(selectAllTextContainer.text()).toBe('Select 2 records')
      })

      it('should not display text when no item is selected', async () => {
        await wrapper.setData({
          pagination: {
            count: 0
          },
          selectedIds: {}
        })
        const selectedIdsCounter = await wrapper.find('.task-record-review-list__container__selected-results')
        expect(selectedIdsCounter.exists()).toBe(false)
      })

      it('should show 1 selected result on open task', async () => {
        await wrapper.setData({
          pagination: {
            count: 0
          },
          selectedIds: {
            1: {}
          }
        })
        const selectedIdsCounter = await wrapper.find('.task-record-review-list__container__selected-results')
        expect(selectedIdsCounter.exists()).toBeTruthy()
        expect(selectedIdsCounter.text()).toBe('1 result selected')
      })

      it('should show 2 selected results on open task', async () => {
        await wrapper.setData({
          pagination: {
            count: 0
          },
          selectedIds: {
            1: {},
            2: {}
          }
        })
        const selectedIdsCounter = await wrapper.find('.task-record-review-list__container__selected-results')
        expect(selectedIdsCounter.exists()).toBeTruthy()
        expect(selectedIdsCounter.text()).toBe('2 results selected')
      })

      it('should show 2 selected results (1 of which is locked)', async () => {
        await wrapper.vm.selectTaskRecordReview('38', true)

        expect(wrapper.vm.isTaskRecordReviewLocked('38')).toBeTruthy()
        expect(wrapper.vm.hasSelectedRecords).toBeTruthy()

        const selectedIdsCounter = await wrapper.find('.task-record-review-list__container__selected-results')
        expect(selectedIdsCounter.exists()).toBeTruthy()
        expect(selectedIdsCounter.text()).toBe('1 result selected (1 of which is locked)')
      })
    })

    describe('Selection on not opened task', () => {
      it('should show 2 selected results (2 of which are locked)', async () => {
        await wrapper.vm.selectTaskRecordReview('38', true)

        expect(wrapper.vm.isTaskRecordReviewLocked('38')).toBeTruthy()
        expect(wrapper.vm.hasSelectedRecords).toBeTruthy()

        const selectedIdsCounter = await wrapper.find('.task-record-review-list__container__selected-results')
        expect(selectedIdsCounter.exists()).toBeTruthy()
        expect(selectedIdsCounter.text()).toBe('1 result selected (1 of which is locked)')
      })
    })
  })

  describe('Update actions according to task status', () => {
    let wrapper
    beforeEach(async () => {
      const attachTo = createContainer()
      const localVue = createLocalVue()

      // Configure the local vue
      const core = await Core.init(localVue).useAll()
      const {i18n, wait, store, router} = core
      const propsData = {taskId: '1'}
      const stubs = ['router-link', 'app-waiter']
      // Finally, instanciate the component
      const options = {
        i18n,
        attachTo,
        localVue,
        propsData,
        router,
        stubs,
        store,
        wait
      }
      wrapper = await shallowMount(TaskRecordReviewList, options)
      await wrapper.vm.setup()
      await wrapper.setData({selectedIds: {1: {}}}) // to have selected data
    })
    afterEach(async () => {
      Task.deleteAll()
    })

    it('should enable bulk choice form when task is opened', async () => {
      await Task.update({where: '1', data: {status: 'OPEN'}})

      // bulk form
      expect(wrapper.vm.isBulkSelectChoiceFormDisabled).toBeFalsy()
      const element = await wrapper.find('task-record-review-bulk-choice-form-stub')
      expect(element.exists()).toBeTruthy()
      expect(element.attributes('disabled')).toBeFalsy()
    })

    it('should disable bulk choice form when task is locked ', async () => {
      expect(wrapper.vm.task.status).toBe('LOCKED')

      // bulk form
      expect(wrapper.vm.isBulkSelectChoiceFormDisabled).toBeTruthy()
      const element = await wrapper.find('task-record-review-bulk-choice-form-stub')
      expect(element.exists()).toBeTruthy()
      expect(element.attributes('disabled')).toBeTruthy()
    })

    it('should disable bulk choice form when task is closed ', async () => {
      await Task.update({where: '1', data: {status: 'CLOSED'}})

      // bulk form
      expect(wrapper.vm.isBulkSelectChoiceFormDisabled).toBeTruthy()
      const element = await wrapper.find('task-record-review-bulk-choice-form-stub')
      expect(element.exists()).toBeTruthy()
      expect(element.attributes('disabled')).toBeTruthy()
    })
  })
})
