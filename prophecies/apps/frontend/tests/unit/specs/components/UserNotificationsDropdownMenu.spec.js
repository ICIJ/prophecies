import { createLocalVue, mount } from '@vue/test-utils'
import { server, rest } from '../../mocks/server'
import '@/store'
import Core from '@/core'
import UserNotification from '@/models/UserNotification'
import UserNotificationLink from '@/components/UserNotificationLink'
import UserNotificationsDropdownMenu from '@/components/UserNotificationsDropdownMenu'

jest.useFakeTimers()

describe('UserNotificationsDropdownMenu', () => {

  function createContainer() {
    const div = document.createElement('div')
    document.body.appendChild(div)
    return div
  }

  describe('with two read notifications', () => {
    let wrapper

    beforeEach(async () => {
      const attachTo = createContainer()
      const localVue = createLocalVue()
      const stubs = ['app-waiter']
      UserNotification.insert({ data: { read: true } })
      UserNotification.insert({ data: { read: true } })
      // Configure the local vue with plugins
      const { i18n, store, wait } = Core.init(localVue).useAll()
      wrapper = mount(UserNotificationsDropdownMenu, { attachTo, localVue, i18n, store, stubs, wait })      
      jest.advanceTimersByTime(1e6)
    })

    afterEach(() => {
      wrapper.destroy()
      UserNotification.deleteAll()
    })

    it('should show two notifications', () => {
      const notifications = wrapper.findAllComponents(UserNotificationLink)
      expect(notifications).toHaveLength(2)
    })

    it('should disable the button to mark all notifications as read', () => {
      const markAllButton = wrapper.find('.user-notifications-dropdown-menu__mark-all')
      expect(markAllButton.attributes('disabled')).toBeTruthy()
    })
  })

  describe('with zero notifications', () => {
    let wrapper

    beforeEach(async () => {
      // Mock notifications endpoint to return nothing
      server.use(rest.get('/api/v1/user-notifications', (req, res, ctx) => {
        return res.once(ctx.json({ data: [] }))
      }))
      const attachTo = createContainer()
      const localVue = createLocalVue()
      const stubs = ['app-waiter']
      // Configure the local vue with plugins
      const { i18n, store, wait } = Core.init(localVue).useAll()
      store.dispatch('entities/deleteAll')
      wrapper = mount(UserNotificationsDropdownMenu, { attachTo, localVue, i18n, store, stubs, wait })
      jest.advanceTimersByTime(1e6)
    })

    afterEach(() => {
      wrapper.destroy()
      server.resetHandlers()
      UserNotification.deleteAll()
    })

    it('should show zero notifications', () => {
      const notifications = wrapper.findAllComponents(UserNotificationLink)
      expect(notifications).toHaveLength(0)
    })

    it('should disable the button to mark all notifications as read', () => {
      const markAllButton = wrapper.find('.user-notifications-dropdown-menu__mark-all')
      expect(markAllButton.attributes('disabled')).toBeTruthy()
    })
  })


  describe('with two unread notifications', () => {
    let wrapper

    beforeEach(async () => {
      const attachTo = createContainer()
      const localVue = createLocalVue()
      const stubs = ['app-waiter']
      // Configure the local vue with plugins
      const { i18n, store, wait } = Core.init(localVue).useAll()
      UserNotification.insert({ data: { read: false } })
      UserNotification.insert({ data: { read: false } })
      wrapper = mount(UserNotificationsDropdownMenu, { attachTo, localVue, i18n, store, stubs, wait })
      jest.advanceTimersByTime(1e6)
    })

    afterEach(() => {
      wrapper.destroy()
      UserNotification.deleteAll()
    })

    it('should show two notifications', () => {
      const notifications = wrapper.findAllComponents(UserNotificationLink)
      expect(notifications).toHaveLength(2)
    })

    it('should enable the button to mark all notifications as read', () => {
      const markAllButton = wrapper.find('.user-notifications-dropdown-menu__mark-all')
      expect(markAllButton.attributes('disabled')).toBeFalsy()
    })
  })
})
