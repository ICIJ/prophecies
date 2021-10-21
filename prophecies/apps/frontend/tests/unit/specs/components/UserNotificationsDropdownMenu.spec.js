import { createLocalVue, mount } from '@vue/test-utils'
import { server, rest } from '../../mocks/server'
import '@/store'
import Core from '@/core'
import UserNotification from '@/models/UserNotification'
import UserNotificationsDropdownMenu from '@/components/UserNotificationsDropdownMenu'

jest.useFakeTimers()

describe('UserNotificationsDropdownMenu', () => {
  // eslint-disable-next-line space-before-function-paren
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
      const stubs = ['b-dropdown-item', 'b-dropdown-text', 'app-waiter']
      // Configure the local vue with plugins
      const { i18n, store, wait } = Core.init(localVue).useAll()
      wrapper = mount(UserNotificationsDropdownMenu, { attachTo, localVue, i18n, store, stubs, wait })
      await wrapper.vm.fetchNotifications()
    })

    it('should NOT show the no notifications message', () => {
      const message = wrapper.find('.user-notifications-dropdown-menu__empty')
      expect(message.exists()).toBeFalsy()
    })

    it('should show two notifications', () => {
      const notifications = wrapper.findAll('.user-notifications-dropdown-menu__list__item')
      expect(notifications).toHaveLength(2)
    })

    it('should show the first notification with the right content', () => {
      const first = wrapper.findAll('.user-notifications-dropdown-menu__list__item__link__description').at(0)
      expect(first.text()).toBe('Django mentioned you in a tip')
    })

    it('should show the second notification with the right content', () => {
      const first = wrapper.findAll('.user-notifications-dropdown-menu__list__item__link__description').at(1)
      expect(first.text()).toBe('Django mentioned you in a note')
    })

    it('should enable the "mark all as read button" button', () => {
      const markAllButton = wrapper.find('.user-notifications-dropdown-menu__read_all--mark_all')
      expect(markAllButton.attributes('disabled')).toBeFalsy()
    })

    it('should show the chip indicating the notification is unread', () => {
      const unreadChip = wrapper.findAll('.user-notifications-dropdown-menu__list__item--unread')
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
      const stubs = ['b-dropdown-item', 'b-dropdown-text', 'app-waiter']
      // Configure the local vue with plugins
      const { i18n, store, wait } = Core.init(localVue).useAll()
      store.dispatch('entities/deleteAll')
      wrapper = mount(UserNotificationsDropdownMenu, { attachTo, localVue, i18n, store, stubs, wait })
    })

    it('should show the no notifications message', () => {
      const message = wrapper.find('.user-notifications-dropdown-menu__empty')
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
      wrapper = mount(UserNotificationsDropdownMenu, { attachTo, localVue, i18n, store, stubs, wait })
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

  describe('All notifications are read', () => {
    let wrapper
    beforeEach(async () => {
      const attachTo = createContainer()

      const localVue = createLocalVue()
      const stubs = ['b-dropdown-item', 'b-dropdown-text', 'app-waiter']
      // Configure the local vue with plugins
      const { i18n, store, wait } = Core.init(localVue).useAll()
      wrapper = mount(UserNotificationsDropdownMenu, { attachTo, localVue, i18n, store, stubs, wait })
      server.use(rest.get('/api/v1/user-notifications', (req, res, ctx) => {
        return res(
          ctx.status(200),
          ctx.json({
            links: {
              first: 'http://localhost/api/v1/user-notifications/?page%5Bnumber%5D=1',
              last: 'http://localhost/api/v1/user-notifications/?page%5Bnumber%5D=1',
              next: null,
              prev: null
            },
            data: [
              {
                type: 'Notification',
                id: '4',
                attributes: {
                  read: true,
                  readAt: '2021-09-02T14:03:27.635214Z'
                },
                relationships: {
                  recipient: {
                    data: {
                      type: 'User',
                      id: '2'
                    }
                  },
                  action: {
                    data: {
                      type: 'Action',
                      id: '91'
                    }
                  }
                },
                links: {
                  self: 'http://localhost/api/v1/user-notifications/4/'
                }
              },
              {
                type: 'Notification',
                id: '1',
                attributes: {
                  read: true,
                  readAt: '2021-09-02T14:03:27.635214Z'
                },
                relationships: {
                  recipient: {
                    data: {
                      type: 'User',
                      id: '2'
                    }
                  },
                  action: {
                    data: {
                      type: 'Action',
                      id: '86'
                    }
                  }
                },
                links: {
                  self: 'http://localhost/api/v1/user-notifications/1/'
                }
              }
            ],
            included: [
              {
                type: 'Action',
                id: '86',
                attributes: {
                  verb: 'mentioned',
                  data: null,
                  public: true,
                  description: null,
                  timestamp: '2021-09-01T19:27:39.502275Z'
                },
                relationships: {
                  actor: {
                    data: {
                      type: 'User',
                      id: '2'
                    }
                  },
                  actionObject: {
                    data: {
                      type: 'Tip',
                      id: '1'
                    }
                  },
                  target: {
                    data: {
                      type: 'User',
                      id: '2'
                    }
                  }
                },
                links: {
                  self: 'http://localhost/api/v1/actions/86/'
                }
              },
              {
                type: 'Action',
                id: '91',
                attributes: {
                  verb: 'mentioned',
                  data: null,
                  public: true,
                  description: null,
                  timestamp: '2021-09-01T21:14:10.562340Z'
                },
                relationships: {
                  actor: {
                    data: {
                      type: 'User',
                      id: '2'
                    }
                  },
                  actionObject: {
                    data: {
                      type: 'TaskRecordReview',
                      id: '38'
                    }
                  },
                  target: {
                    data: {
                      type: 'User',
                      id: '2'
                    }
                  }
                },
                links: {
                  self: 'http://localhost/api/v1/actions/91/'
                }
              },
              {
                type: 'User',
                id: '2',
                attributes: {
                  url: 'http://localhost/api/v1/users/2/',
                  firstName: 'Django',
                  lastName: '',
                  username: 'django',
                  email: 'support@icij.org',
                  emailMd5: 'd159b514bfc6e718ac0a4ed0487d4d3e',
                  isStaff: true
                },
                links: {
                  self: 'http://localhost/api/v1/users/2/'
                }
              }
            ],
            meta: {
              pagination: {
                page: 1,
                pages: 1,
                count: 2
              }
            }
          })
        )
      }))
      await wrapper.vm.fetchNotifications()
    })

    afterEach(() => {
      server.resetHandlers()
      UserNotification.deleteAll()
    })

    it('should mark all notification as read', async () => {
      const markAllButton = wrapper.find('.user-notifications-dropdown-menu__read_all--mark_all')
      expect(markAllButton.attributes('disabled')).toBeTruthy()
      const unreadChip = wrapper.find('.user-notifications-dropdown-menu__list__item--unread')
      expect(unreadChip.exists()).toBeFalsy()
    })
  })
})
