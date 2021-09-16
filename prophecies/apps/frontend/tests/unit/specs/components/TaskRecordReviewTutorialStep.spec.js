import {
  createLocalVue,
  mount
} from '@vue/test-utils'
import Core from '@/core'

import TaskRecordReviewTutorialStep from '@/components/TaskRecordReviewTutorialStep'
describe('TaskRecordReviewTutorialStep', () => {
  let wrapper

  function createContainer () {
    const div = document.createElement('div')
    document.body.appendChild(div)
    return div
  }

  beforeEach(() => {
    const attachTo = createContainer()
    const localVue = createLocalVue()
    Core.init(localVue).useAll()

    const propsData = {
      number: 1,
      step:
        {
          text: 'Read the content to be checked',
          class: 'offset-2 col-8 ',
          width: '130px'
        },
      stepCount: 5
    }
    // Configure the local vue with plugins
    wrapper = mount(TaskRecordReviewTutorialStep, {
      attachTo,
      localVue,
      propsData
    })
  })
  it('should show step numbers 1/5', () => {
    const tutorialProgressNumbers = wrapper.find('.task-record-review-tutorial-step__progression__numbers')
    expect(tutorialProgressNumbers.text()).toBe('1/5')
  })
  it('should show 20% progress', () => {
    const tutorialProgressBar = wrapper.find('.task-record-review-tutorial-step__progression__bar-position .progress .progress-bar')
    expect(tutorialProgressBar.attributes().style).toBe('width: 20%;')
  })
  it('should show the text of the current task', () => {
    const tutorialStepText = wrapper.find('.task-record-review-tutorial-step__text-content')
    expect(tutorialStepText.text()).toBe('Read the content to be checked')
  })
})
