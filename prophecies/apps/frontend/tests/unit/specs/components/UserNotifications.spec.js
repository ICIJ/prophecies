import { createLocalVue, mount } from '@vue/test-utils'
import { server, rest } from '../../mocks/server'
import '@/store'
import Core from '@/core'
import UserNotifications from '@/components/UserNotifications'

jest.useFakeTimers()

describe('UserNotifications', () => {
  function createContainer() {
    const div = document.createElement('div')
    document.body.appendChild(div)
    return div
  }

  describe('with two notifications', () => {
    let wrapper

    beforeEach(async () => {
      const attachTo = createContainer()
      const localVue = createLocalVue()
      const stubs = ['app-waiter']
      // Configure the local vue with plugins
      const { i18n, store, wait } = Core.init(localVue).useAll()
      wrapper = mount(UserNotifications, { attachTo, localVue, i18n, store, stubs, wait })
      await wrapper.vm.fetchNotifications()
    })

    it('should NOT show the no notifications message', () => {
      const message = wrapper.find('.user-notifications__empty')
      expect(message.exists()).toBeFalsy()
    })

    it('should show two notifications', () => {
      const notifications = wrapper.findAll('.user-notification-link')
      expect(notifications).toHaveLength(2)
    })

    it('should show the first notification with the right content', () => {
      const first = wrapper.findAll('.user-notification-link__description').at(0)
      expect(first.text()).toBe('Django mentioned you in a tip')
    })

    it('should show the second notification with the right content', () => {
      const first = wrapper.findAll('.user-notification-link__description').at(1)
      expect(first.text()).toBe('Django mentioned you in a note')
    })

    it('should show the chip indicating the notification is unread', () => {
      const unreadChip = wrapper.findAll('.user-notification-link__unread-bullet')
      expect(unreadChip).toHaveLength(1)
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
      wrapper = mount(UserNotifications, { attachTo, localVue, i18n, store, stubs, wait })
    })

    it('should show the no notifications message', () => {
      const message = wrapper.find('.user-notifications__empty')
      expect(message.exists()).toBeTruthy()
    })
  })

  describe('reload notification periodicaly', () => {
    let spyFetchNotifications
    let wrapper

    beforeEach(async () => {
      const attachTo = createContainer()

      const localVue = createLocalVue()
      const stubs = ['b-dropdown-item', 'b-dropdown-text', 'app-waiter']
      // Configure the local vue with plugins
      const { i18n, store, wait } = Core.init(localVue).useAll()
      wrapper = mount(UserNotifications, { attachTo, localVue, i18n, store, stubs, wait })
      spyFetchNotifications = jest.spyOn(wrapper.vm, 'fetchNotifications')
      await wrapper.vm.fetchNotifications()
    })

    afterEach(() => {
      spyFetchNotifications.mockRestore()
    })

    it('should reload planFetchNotifications after 10s', async () => {
      expect(spyFetchNotifications).toHaveBeenCalledTimes(1)
      jest.advanceTimersByTime(10000)
      expect(spyFetchNotifications).toHaveBeenCalledTimes(2)
      jest.advanceTimersByTime(10000)
      expect(spyFetchNotifications).toHaveBeenCalledTimes(3)
    })

    it('should stop reloading notifications after the component is destroyed', async () => {
      expect(spyFetchNotifications).toHaveBeenCalledTimes(1)
      jest.advanceTimersByTime(10000)
      expect(spyFetchNotifications).toHaveBeenCalledTimes(2)
      wrapper.destroy()
      jest.advanceTimersByTime(10000)
      expect(spyFetchNotifications).toHaveBeenCalledTimes(2)
    })
  })
})
