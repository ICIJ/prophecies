import { createLocalVue, mount } from '@vue/test-utils'
import '@/store'
import Core from '@/core'
import NotificationsDropdownMenu from '@/components/NotificationsDropdownMenu'

describe('NotificationsDropdownMenu', () => {
  function flushPromises () {
    return new Promise(resolve => setTimeout(resolve, 0))
  }

  describe('with two notifications', () => {
    let wrapper

    beforeEach(async () => {
      const localVue = createLocalVue()
      const stubs = ['b-dropdown-item', 'b-dropdown-text', 'app-waiter']
      // Configure the local vue with plugins
      const { i18n, store, wait } = Core.init(localVue).useAll()
      wrapper = mount(NotificationsDropdownMenu, { localVue, i18n, store, stubs, wait })
      await wrapper.vm.fetchNotifications()
    })

    it('should NOT show the no notifications message', () => {
      const message = wrapper.find('.notifications-dropdown-menu__empty')
      expect(message.exists()).toBeFalsy()
    })

    it('should show two notifications', () => {
      const notifications = wrapper.findAll('.notifications-dropdown-menu__item')
      expect(notifications).toHaveLength(2)
    })

    it('should show the first notification with the right content', () => {
      const first = wrapper.findAll('.notifications-dropdown-menu__item__link__description').at(0)
      expect(first.text()).toBe('Django mentioned you in a tip')
    })

    it('should show the second notification with the right content', () => {
      const first = wrapper.findAll('.notifications-dropdown-menu__item__link__description').at(1)
      expect(first.text()).toBe('Django mentioned you in a note')
    })
  })

  describe('with zero notifications', () => {
    let wrapper

    beforeEach(async () => {
      const localVue = createLocalVue()
      const stubs = ['b-dropdown-item', 'b-dropdown-text', 'app-waiter']
      // Configure the local vue with plugins
      const { i18n, store, wait } = Core.init(localVue).useAll()
      wrapper = mount(NotificationsDropdownMenu, { localVue, i18n, store, stubs, wait })
      await wrapper.vm.fetchNotifications()
      // Delete all notifications (and other entities)
      store.dispatch('entities/deleteAll')
    })

    it('should show the no notifications message', () => {
      const message = wrapper.find('.notifications-dropdown-menu__empty')
      expect(message.exists()).toBeTruthy()
    })
  })
})
