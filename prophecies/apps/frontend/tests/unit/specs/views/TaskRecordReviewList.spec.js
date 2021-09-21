import {
  createLocalVue,
  shallowMount
} from '@vue/test-utils'
import Core from '@/core'
import ChoiceGroup from '@/models/ChoiceGroup'
import Task from '@/models/Task'
import TaskRecordReview from '@/models/TaskRecordReview'
import TaskRecord from '@/models/TaskRecord'
import User from '@/models/User'
import TaskRecordReviewList from '@/views/TaskRecordReviewList'
describe('TaskRecordReviewList', () => {
  let wrapper

  function createContainer () {
    const div = document.createElement('div')
    document.body.appendChild(div)
    return div
  }

  beforeAll(async () => {
    await ChoiceGroup.api().get()
    await Task.api().get()
    await TaskRecordReview.api().get('')
    await TaskRecord.api().get()
    await User.api().me()
  })

  beforeEach(async () => {
    const attachTo = createContainer()
    const localVue = createLocalVue()

    // Configure the local vue
    const core = await Core.init(localVue).useAll()
    const {
      i18n,
      wait,
      store,
      router
    } = core
    const propsData = {
      taskId: '1'
    }

    const stubs = ['router-link', 'router-view', 'app-waiter']
    await core.configure()
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
    await new Promise(resolve => setTimeout(resolve))
  })

  afterEach(async () => {
    // Prevent a Vue warning in the next tick when the parentNode doesnt exist:
    // > TypeError: Cannot read property 'createElement' of null
    // @see https://stackoverflow.com/a/62262333
    wrapper.destroy()
  })

  it('should not display text when no item is selected', async () => {
    await wrapper.setData({
      pagination: {
        count: 0
      },
      selectedIds: {
      }
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
    expect(selectedIdsCounter.exists()).toBe(true)
    expect(selectedIdsCounter.text()).toBe('1 result selected')
  })
  //
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
    expect(selectedIdsCounter.exists()).toBe(true)
    expect(selectedIdsCounter.text()).toBe('2 results selected')
  })

  it('should show 2 selected results (1 of which is locked)', async () => {
    const response = await wrapper.vm.fetchTaskRecordReviews()
    await wrapper.vm.selectTaskRecordReview('38', true)

    expect(wrapper.vm.isTaskRecordReviewLocked('38')).toBe(true)
    expect(wrapper.vm.hasSelectedRecords).toBe(true)

    const selectedIdsCounter = await wrapper.find('.task-record-review-list__container__selected-results')
    expect(selectedIdsCounter.exists()).toBe(true)
    expect(selectedIdsCounter.text()).toBe('1 result selected (1 of which is locked)')
  })
})
