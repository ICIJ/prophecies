import { createLocalVue, mount } from '@vue/test-utils'
import AppHeader from '@/components/AppHeader'
import Core from '@/core'

describe('AppHeader', () => {
  describe('for a staff user', () => {
    let localVue
    let wrapper

    beforeEach(async () => {
      localVue = createLocalVue()
      // Mock Core methods that use the backend
      jest.spyOn(Core.prototype, 'getUser').mockResolvedValue({
        username: 'olivia',
        first_name: 'Olivia',
        last_name: 'Reinhardt',
        email: 'engineering@icij.org',
        email_md5: '628e9a99d87799e9d434b63d2c3744ca',
        is_staff: true
      })
      jest.spyOn(Core.prototype, 'getSettings').mockResolvedValue({ foo: 'bar' })
      // Configure the local vue
      const core = Core.init(localVue).useAll()
      await core.configure()
      // Finally, instanciate the component
      wrapper = mount(AppHeader, { i18n: core.i18n, localVue })
    })

    afterEach(() => {
      jest.restoreAllMocks()
    })

    it('should display the full name of the user', () => {
      expect(wrapper.find('.app-header__nav-right__user__display-name').text()).toBe('Olivia Reinhardt')
    })

    it('should build an avatar URL using the email_md5', () => {
      const src = wrapper.find('.app-header__nav-right__user__avatar').attributes('src')
      expect(src).toBe('https://www.gravatar.com/avatar/628e9a99d87799e9d434b63d2c3744ca')
    })

    it('should display a link to the admin if the user is staff', () => {
      expect(wrapper.find('.app-header__nav-right__user__admin').exists()).toBeTruthy()
    })
  })

  describe('for a non-staff user with no last name', () => {
    let localVue
    let wrapper

    beforeEach(async () => {
      localVue = createLocalVue()
      // Mock Core methods that use the backend
      jest.spyOn(Core.prototype, 'getUser').mockResolvedValue({
        username: 'django',
        first_name: 'Django',
        last_name: '',
        email: 'support@icij.org',
        email_md5: 'd159b514bfc6e718ac0a4ed0487d4d3e',
        is_staff: false
      })
      jest.spyOn(Core.prototype, 'getSettings').mockResolvedValue({ foo: 'bar' })
      // Configure the local vue
      const core = Core.init(localVue).useAll()
      await core.configure()
      // Finally, instanciate the component
      wrapper = mount(AppHeader, { i18n: core.i18n, localVue })
    })

    afterEach(() => {
      jest.restoreAllMocks()
    })

    it('should display the username of the user', () => {
      expect(wrapper.find('.app-header__nav-right__user__display-name').text()).toBe('django')
    })

    it('should not display a link to the admin if the user isnt staff', () => {
      expect(wrapper.find('.app-header__nav-right__user__admin').exists()).toBeFalsy()
    })
  })
})
