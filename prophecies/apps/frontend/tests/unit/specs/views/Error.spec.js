import { createLocalVue, shallowMount } from '@vue/test-utils'

import { Core } from '@/core'
import User from '@/models/User'
import Error from '@/views/Error'

const { i18n, localVue } = Core.init(createLocalVue()).useAll()

describe('Error', () => {
  let spyUserMe
  let attachTo

  function createContainer() {
    const div = document.createElement('div')
    document.body.appendChild(div)
    return div
  }

  beforeAll(() => {
    spyUserMe = jest.spyOn(User, 'me')
  })

  beforeEach(() => {
    // WHen using `v-b-tooltip` directive, you must attached your component to a
    // child element of the document's body.
    attachTo = createContainer()
  })

  afterAll(() => {
    spyUserMe.mockRestore()
  })

  it('should display a custom title', () => {
    const propsData = { title: 'This is wrong!' }
    const wrapper = shallowMount(Error, { i18n, localVue, propsData, attachTo })
    expect(wrapper.find('.error__container__heading').text()).toBe('This is wrong!')
  })

  it('should display the error code', () => {
    const propsData = { code: 404, title: 'Page not found' }
    const wrapper = shallowMount(Error, { i18n, localVue, propsData, attachTo })
    expect(wrapper.find('.error__container__heading__code__value').text()).toBe('404')
  })

  it('should not display an error code', () => {
    const propsData = { title: 'Page not found' }
    const wrapper = shallowMount(Error, { i18n, localVue, propsData, attachTo })
    expect(wrapper.find('.error__container__heading__code__value').text()).toBe('')
  })

  it('should display the default description text', () => {
    const defaultDescription = i18n.t('error.description')
    const propsData = { title: 'Something went wrong' }
    const wrapper = shallowMount(Error, { i18n, localVue, propsData, attachTo })
    expect(wrapper.find('.error__container__description').text()).toBe(defaultDescription)
  })

  it('should display a custom description text', () => {
    const propsData = { title: 'Something went wrong', description: 'Broken :/' }
    const wrapper = shallowMount(Error, { i18n, localVue, propsData, attachTo })
    expect(wrapper.find('.error__container__description').text()).toBe('Broken :/')
  })

  it('should display a header when user is logged in', async () => {
    // Mock the user session
    spyUserMe.mockReturnValue({ username: 'foo' })
    const wrapper = shallowMount(Error, { i18n, localVue, attachTo })
    // Render again
    expect(wrapper.find('.error__header').exists()).toBeTruthy()
  })

  it('should not display a header when user is logged out', async () => {
    // Mock the empty user session
    spyUserMe.mockReturnValue(null)
    const wrapper = shallowMount(Error, { i18n, localVue, attachTo })
    // Render again
    expect(wrapper.find('.error__header').exists()).toBeFalsy()
  })
})
