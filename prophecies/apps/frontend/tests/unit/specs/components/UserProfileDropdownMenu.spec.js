import {createLocalVue, shallowMount} from '@vue/test-utils'

import '@/store'
import Core from '@/core'
import {rest, server} from '../../mocks/server'
import User from '@/models/User'

import UserProfileDropdownMenu from '@/components/UserProfileDropdownMenu'

describe('UserProfileDropdownMenu', () => {
  let wrapper

  afterEach(async () => {
    server.resetHandlers()
    User.deleteAll()
  })

  describe('User is not a staff member', () => {
    beforeAll(async () => {
      const localVue = createLocalVue()
      // Mock current user
      server.use(rest.get('/api/v1/users/me/', (req, res, ctx) => {
        return res.once(ctx.json({
          data: {
            id: 20,
            attributes: {
              username: 'olivia',
              firstName: 'Olivia',
              lastName: 'Reinhardt',
              email: 'engineering@icij.org',
              emailMd5: '628e9a99d87799e9d434b63d2c3744ca',
              isStaff: false
            }
          }
        }))
      }))
      // Configure the local vue with plugins
      const core = Core.init(localVue).useAll()
      const {i18n} = core
      await core.configure()
      wrapper = shallowMount(UserProfileDropdownMenu, {localVue, i18n})
    })
    it('should have 10 entries', async () => {
      expect(wrapper.findAll('b-dropdown-item-stub')).toHaveLength(10)
    })
  })
  describe('User is a staff member', () => {
    let wrapper

    beforeAll(async () => {
      const localVue = createLocalVue()
      // Mock current user
      server.use(rest.get('/api/v1/users/me/', (req, res, ctx) => {
        return res.once(ctx.json({
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
        }))
      }))
      // Configure the local vue with plugins
      const core = Core.init(localVue).useAll()
      const {i18n} = core
      await core.configure()

      wrapper = shallowMount(UserProfileDropdownMenu, {localVue, i18n})
    })
    it("should mount the olivia's user profile menu", () => {
      expect(wrapper.vm.user.username).toBe('olivia')
      expect(wrapper.vm.user.isStaff).toBe(true)
    })
    it('should have 11 entries', () => {
      expect(wrapper.vm.user.isStaff).toBe(true)
      expect(wrapper.findAll('b-dropdown-item-stub')).toHaveLength(11)
    })
  })
})
