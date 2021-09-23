import {
  createLocalVue,
  shallowMount
} from '@vue/test-utils'
import Core from '@/core'
import TaskRecordReviewList from '@/views/TaskRecordReviewList'

describe('TaskRecordReviewList', () => {
  let wrapper

  function createContainer () {
    const div = document.createElement('div')
    document.body.appendChild(div)
    return div
  }

  beforeEach(async () => {
    const attachTo = createContainer()
    const localVue = createLocalVue()

    // Configure the local vue
    const core = await Core.init(localVue).useAll()
    const { i18n, wait, store, router } = core
    const propsData = { taskId: '1' }
    const stubs = ['router-link', 'app-waiter']
    // Finally, instanciate the component
    wrapper = await shallowMount(TaskRecordReviewList, {
      i18n,
      attachTo,
      localVue,
      propsData,
      router,
      stubs,
      store,
      wait
    })
    await wrapper.vm.setup()
  })

  it('should display "Select all records" or "Select 1 record" according to the number of records', async () => {
    await wrapper.setData({
      pagination: {
        count: 0
      },
      selectedIds: { },
      taskRecordReviewIds: ['38']
    })
    let selectAllTextContainer = await wrapper.find('.task-record-review-list__container__select-all')
    expect(selectAllTextContainer.text()).toBe("Select 1 record")
    await wrapper.setData({
      pagination: {
        count: 0
      },
      selectedIds: { },
      taskRecordReviewIds: ['38','37']
    })
    selectAllTextContainer = await wrapper.find('.task-record-review-list__container__select-all')
    expect(selectAllTextContainer.text()).toBe("Select 2 records")
  })


  it('should not display text when no item is selected', async () => {
    await wrapper.setData({
      pagination: {
        count: 0
      },
      selectedIds: { }
    })
    const selectedIdsCounter = await wrapper.find('.task-record-review-list__container__selected-results')
    expect(selectedIdsCounter.exists()).toBe(false)
  })

  it('should show 1 selected result', async () => {
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

  it('should show 2 selected results', async () => {
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
