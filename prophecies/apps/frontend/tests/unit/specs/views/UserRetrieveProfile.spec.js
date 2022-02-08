import { createLocalVue, shallowMount } from '@vue/test-utils'

import '@/store'
import Core from '@/core'
import { server, rest } from '../../mocks/server'
import User from '@/models/User'

import UserRetrieveProfile from '@/views/UserRetrieveProfile'
import UserCard from '@/components/UserCard'

describe('UserRetrieveProfile', () => {
  let wrapper

  beforeAll(async () => {
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
            lastLogin: '2022-02-04T17:41:43.040505Z',
            isStaff: true,
            isSuperuser: true
          }
        }
      }))
    }))
  })

  beforeEach(async () => {
    const localVue = createLocalVue()
    const core = Core.init(localVue).useAll()
    const { i18n, wait, store, router } = core
    const stubs = ['router-link', 'app-waiter']
    const propsData = { username: 'olivia' }
    const options = {
      i18n,
      localVue,
      propsData,
      store,
      stubs,
      router,
      wait
    }
    await core.configure()
    wrapper = await shallowMount(UserRetrieveProfile, options)
  })

  afterEach(async () => {
    await wrapper.destroy()
  })

  it('should display user profile', async () => {
    expect(wrapper.findComponent(UserCard).exists()).toBe(true)
  })

  it('should display user info: email and last login date', async () => {
    expect(wrapper.find('.user-retrieve-profile__email').text()).toBe('Email: engineering@icij.org')
    expect(wrapper.find('.user-retrieve-profile__last-login').text()).toBe('Last login: Fri 04, Feb 2022 - 5:02pm') // jest is running in UTC TZ
  })

  it('should show super user badge', async () => {
    expect(wrapper.find('.user-retrieve-profile__super-user').exists()).toBeTruthy()
    User.update({ where: 20, data: { isSuperuser: false } })
    await wrapper.vm.$nextTick()
    expect(wrapper.find('.user-retrieve-profile__super-user').exists()).toBeFalsy()
  })
})
