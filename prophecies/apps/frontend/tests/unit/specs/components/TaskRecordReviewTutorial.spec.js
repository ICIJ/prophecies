import {
  createLocalVue,
  mount
} from '@vue/test-utils'
import Core from '@/core'

import TaskRecordReviewTutorial from '@/components/TaskRecordReviewTutorial'

describe('TaskRecordReviewTutorial', () => {
  let wrapper

  function createContainer() {
    const div = document.createElement('div')
    document.body.appendChild(div)
    return div
  }

  beforeEach(() => {
    const attachTo = createContainer()
    const localVue = createLocalVue()
    // Configure the local vue
    const core = Core.init(localVue).useAll()
    const {i18n} = core
    // Configure the local vue with plugins
    wrapper = mount(TaskRecordReviewTutorial, {
      attachTo,
      i18n,
      localVue
    })
  })

  it('should show the tutorial', () => {
    expect(wrapper.vm.showTutorial).toBe(true)
    expect(wrapper.vm.stepNumber).toBe(1)
    const tutorialCard = wrapper.find('.task-record-review-tutorial')
    expect(tutorialCard.exists()).toBe(true)
    expect(tutorialCard.isVisible()).toBe(true)
  })

  it('should hide the tutorial', async () => {
    await wrapper.setData({showTutorial: false})
    const tutorialCard = wrapper.find('.task-record-review-tutorial')
    expect(tutorialCard.exists()).toBe(true)
    expect(tutorialCard.isVisible()).toBe(false)
  })

  it('should not show "previous" button on first step', async () => {
    let previousStepExists = wrapper.find('.task-record-review-tutorial-card__buttons__previous')
    expect(previousStepExists.exists()).toBe(false)
    await wrapper.setData({stepNumber: 2})
    previousStepExists = wrapper.find('.task-record-review-tutorial-card__buttons__previous')
    expect(previousStepExists.exists()).toBe(true)
  })

  it('should show skip and next except on last step where "close" button replaces next button', async () => {
    let closeStepExists = wrapper.find('.task-record-review-tutorial-card__buttons__close')
    expect(closeStepExists.exists()).toBe(false)
    let nextStepExists = wrapper.find('.task-record-review-tutorial-card__buttons__next')
    expect(nextStepExists.exists()).toBe(true)
    let skipTutorialExists = wrapper.find('.task-record-review-tutorial-card__buttons__skip')
    expect(skipTutorialExists.exists()).toBe(true)
    await wrapper.setData({stepNumber: 5})
    closeStepExists = wrapper.find('.task-record-review-tutorial-card__buttons__close')
    expect(closeStepExists.exists()).toBe(true)
    nextStepExists = wrapper.find('.task-record-review-tutorial-card__buttons__next')
    expect(nextStepExists.exists()).toBe(false)
    skipTutorialExists = wrapper.find('.task-record-review-tutorial-card__buttons__skip')
    expect(skipTutorialExists.exists()).toBe(false)
  })
})
