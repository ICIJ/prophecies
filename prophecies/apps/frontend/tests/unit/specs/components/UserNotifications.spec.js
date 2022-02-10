import { createLocalVue, mount } from '@vue/test-utils'
import { server, rest } from '../../mocks/server'

import '@/store'
import Core from '@/core'
import UserNotifications from '@/components/UserNotifications'
import UserNotification from '@/models/UserNotification'

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

      const { response } = await UserNotification.api().get('')
      const notificationIds = response.data.data.map(t => t.id)
      const propsData = { notificationIds }

      wrapper = mount(UserNotifications, { attachTo, localVue, i18n, propsData, store, stubs, wait })
    })


    it('should NOT show the "no notifications" message', () => {
      const message = wrapper.find('.user-notifications__empty')
      expect(message.exists()).toBeFalsy()
    })

    it('should show two notifications', () => {
      const notifications = wrapper.findAll('.user-notification-link')
      expect(notifications).toHaveLength(2)
    })

    it('should show the first notification with the right content', () => {
      const first = wrapper.findAll('.user-notification-link__description').at(0)
      expect(first.text()).toBe('Django mentioned you in a note')
    })

    it('should show the second notification with the right content', () => {
      const first = wrapper.findAll('.user-notification-link__description').at(1)
      expect(first.text()).toBe('Django mentioned you in a tip')
    })

    it('should show the chip indicating the notification is unread', () => {
      const unreadChip = wrapper.findAll('.user-notification-link__unread-bullet')
      expect(unreadChip).toHaveLength(1)
    })
  })

  describe('with zero notifications', () => {
    let wrapper

    beforeEach(async () => {
      const attachTo = createContainer()
      const localVue = createLocalVue()
      const stubs = ['app-waiter']
      // Configure the local vue with plugins
      const { i18n, store, wait } = Core.init(localVue).useAll()
      wrapper = mount(UserNotifications, { attachTo, localVue, i18n, store, stubs, wait })
    })

    it('should show the "no notifications" message', () => {
      const message = wrapper.find('.user-notifications__empty')
      expect(message.exists()).toBeTruthy()
    })
  })
})
