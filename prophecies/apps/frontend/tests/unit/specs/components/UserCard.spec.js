import { createLocalVue, mount } from '@vue/test-utils'
import UserAvatar from '@/components/UserAvatar'
import UserCard from '@/components/UserCard'
import UserLink from '@/components/UserLink'
import User from '@/models/User'
import Core from '@/core'

describe('UserCard', () => {
  let wrapper

  beforeAll(() => {
    User.insert({
      data: {
        id: '2000',
        username: 'fatima',
        firstName: 'Fátima',
        lastName: 'Reinhardt',
        email: 'engineering@icij.org',
        emailMd5: '628e9a99d87799e9d434b63d2c3744ca',
        isStaff: true
      }
    })
  })

  beforeEach(async () => {
    const localVue = createLocalVue()
    const propsData = { userId: '2000' }
    // Configure the local vue
    const core = Core.init(localVue).useAll()
    // Configure the core
    await core.configure()
    // Get router from core
    const { i18n, store, router, wait } = core
    // Mock fetch method to avoid loading data
    UserCard.methods.fetch = () => (null)
    // Finally, instanciate the component
    wrapper = mount(UserCard, { localVue, propsData, i18n, store, router, wait })
  })

  it('should build a card with an avatar', () => {
    expect(wrapper.findComponent(UserAvatar).exists()).toBeTruthy()
  })

  it('should build a card with a link to the user profile', () => {
    expect(wrapper.findComponent(UserLink).exists()).toBeTruthy()
  })
})
