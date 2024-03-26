import { createLocalVue, mount } from '@vue/test-utils'

import { server, rest } from '../../mocks/server'

import AppHeader from '@/components/AppHeader'
import Core from '@/core'
import User from '@/models/User'

describe('AppHeader', () => {
  // eslint-disable-next-line space-before-function-paren
  function createContainer() {
    const div = document.createElement('div')
    document.body.appendChild(div)
    return div
  }
  describe('for a staff user', () => {
    let localVue
    let wrapper

    beforeEach(async () => {
      const attachTo = createContainer()
      localVue = createLocalVue()
      // Mock current user
      server.use(
        rest.get('/api/v1/users/me/', (req, res, ctx) => {
          return res.once(
            ctx.json({
              data: {
                id: 20,
                attributes: {
                  username: 'olivia',
                  firstName: 'Olivia',
                  lastName: 'Reinhardt',
                  email: 'engineering@icij.org',
                  emailMd5: '628e9a99d87799e9d434b63d2c3744ca',
                  isStaff: true
                }
              }
            })
          )
        })
      )
      // Configure the local vue
      const core = Core.init(localVue).useAll()
      const { i18n, store, wait, router } = core
      const stubs = ['router-link', 'app-waiter']
      await core.configure()
      // Finally, instanciate the component
      wrapper = mount(AppHeader, { attachTo, i18n, localVue, stubs, store, wait, router })
    })

    afterEach(async () => {
      server.resetHandlers()
      User.deleteAll()
    })

    it('should display the full name of the user', () => {
      expect(wrapper.find('.app-header__nav-right__user__display-name').text()).toBe('Olivia Reinhardt')
    })

    it('should display a link to the admin if the user is staff', () => {
      expect(wrapper.find('.user-profile-dropdown-menu__item--admin').exists()).toBeTruthy()
    })
  })

  describe('for a non-staff user with no last name', () => {
    let localVue
    let wrapper

    beforeEach(async () => {
      const attachTo = createContainer()
      localVue = createLocalVue()
      // Mock current user
      server.use(
        rest.get('/api/v1/users/me/', (req, res, ctx) => {
          return res.once(
            ctx.json({
              data: {
                id: 20,
                attributes: {
                  username: 'django',
                  firstName: 'Django',
                  lastName: '',
                  email: 'support@icij.org',
                  emailMd5: 'd159b514bfc6e718ac0a4ed0487d4d3e',
                  isStaff: false
                }
              }
            })
          )
        })
      )
      // Configure the local vue
      const core = Core.init(localVue).useAll()
      const { i18n, store, wait } = core
      const stubs = ['router-link', 'app-waiter']
      await core.configure()
      // Finally, instanciate the component
      wrapper = mount(AppHeader, { attachTo, i18n, localVue, stubs, store, wait })
    })

    afterEach(() => {
      server.resetHandlers()
      User.deleteAll()
    })

    it('should display the username of the user', () => {
      expect(wrapper.find('.app-header__nav-right__user__display-name').text()).toBe('django')
    })

    it('should not display a link to the admin if the user isnt staff', () => {
      expect(wrapper.find('.user-profile-dropdown-menu__item--admin').exists()).toBeFalsy()
    })
  })
})
