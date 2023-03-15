import { createLocalVue, mount } from '@vue/test-utils'
import UserAvatar from '@/components/UserAvatar'
import User from '@/models/User'
import Core from '@/core'

describe('UserAvatar', () => {
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
    Core.init(localVue).useAll().configure()
    // Finally, instanciate the component
    wrapper = mount(UserAvatar, { localVue, propsData })
  })

  it('should build an avatar URL using the emailMd5', () => {
    const src = wrapper.attributes('src')
    expect(src).toBe('https://www.gravatar.com/avatar/628e9a99d87799e9d434b63d2c3744ca')
  })
})
