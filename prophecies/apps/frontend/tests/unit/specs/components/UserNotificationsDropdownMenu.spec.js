import { createLocalVue, mount } from '@vue/test-utils'
import { server, rest } from '../../mocks/server'
import '@/store'
import Core from '@/core'
import User from '@/models/User'
import UserNotification from '@/models/UserNotification'
import UserNotificationLink from '@/components/UserNotificationLink'
import UserNotificationsDropdownMenu from '@/components/UserNotificationsDropdownMenu'

jest.useFakeTimers()

describe('UserNotificationsDropdownMenu', () => {

  // Ensure we advance timers and run all pending job
  // in the PromiseJobs queue.
  function advanceTimersByTimeAndFlushPromises(ms) {
    jest.advanceTimersByTime(ms)
    return new Promise(done => jest.requireActual("timers").setTimeout(done, 200))
  }

  function createContainer() {
    const div = document.createElement('div')
    document.body.appendChild(div)
    return div
  }

  describe('with two read notifications', () => {
    let wrapper

    beforeAll(async () => {
      await User.api().me()
    })

    beforeEach(async () => {
      // Mock notifications endpoint to return nothing
      server.use(rest.get('/api/v1/user-notifications', (req, res, ctx) => {
        return res(ctx.json({
          data: [
            { id: '13', attributes: { read: true } },
            { id: '14', attributes: { read: true } }
          ]
        }))
      }))
      const attachTo = createContainer()
      const localVue = createLocalVue()
      const stubs = ['app-waiter']
      // Configure the local vue with plugins
      const { i18n, store, wait } = Core.init(localVue).useAll()
      wrapper = mount(UserNotificationsDropdownMenu, { attachTo, localVue, i18n, store, stubs, wait })
      await advanceTimersByTimeAndFlushPromises(1e4)
    })

    afterEach(() => {
      wrapper.destroy()
      UserNotification.deleteAll()
      server.resetHandlers()
    })

    it('should show two notifications', () => {
      const notifications = wrapper.findAllComponents(UserNotificationLink)
      expect(notifications).toHaveLength(2)
    })

    it('should disable the button to mark all notifications as read', () => {
      const markAllButton = wrapper.find('.user-notifications-dropdown-menu__mark-all')
      expect(markAllButton.attributes('disabled')).toBeTruthy()
    })

    it('should planify a poll to fetch user notification in the store', () => {
      expect(wrapper.vm.$store.state.userNotificationsPoll.pollId).not.toBeNull()
    })
  })

  describe('with zero notifications', () => {
    let wrapper

    beforeAll(async () => {
      await User.api().me()
    })

    beforeEach(async () => {
      // Mock notifications endpoint to return nothing
      server.use(rest.get('/api/v1/user-notifications', (req, res, ctx) => {
        return res(ctx.json({ data: [] }))
      }))
      const attachTo = createContainer()
      const localVue = createLocalVue()
      const stubs = ['app-waiter']
      // Configure the local vue with plugins
      const { i18n, store, wait } = Core.init(localVue).useAll()
      wrapper = mount(UserNotificationsDropdownMenu, { attachTo, localVue, i18n, store, stubs, wait })
      await advanceTimersByTimeAndFlushPromises(1e4)
    })

    afterEach(() => {
      wrapper.destroy()
      UserNotification.deleteAll()
      server.resetHandlers()
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

    beforeAll(async () => {
      await User.api().me()
    })

    beforeEach(async () => {
      // Mock notifications endpoint to return nothing
      server.use(rest.get('/api/v1/user-notifications', (req, res, ctx) => {
        return res(ctx.json({ 
          data: [
            { id: '15', attributes: { read: false } },
            { id: '16', attributes: { read: false } }
          ] 
        }))
      }))
      const attachTo = createContainer()
      const localVue = createLocalVue()
      const stubs = ['app-waiter']
      // Configure the local vue with plugins
      const { i18n, store, wait } = Core.init(localVue).useAll()
      wrapper = mount(UserNotificationsDropdownMenu, { attachTo, localVue, i18n, store, stubs, wait })
      await advanceTimersByTimeAndFlushPromises(1e4)
    })

    afterEach(() => {
      wrapper.destroy()
      UserNotification.deleteAll()
      server.resetHandlers()
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
