import { createLocalVue, mount } from '@vue/test-utils'
import UserLink from '@/components/UserLink'
import User from '@/models/User'
import Core from '@/core'

describe('UserLink', () => {

  function createContainer() {
    const div = document.createElement('div')
    document.body.appendChild(div)
    return div
  }

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

  describe('user link without slot', () => {
    let wrapper

    beforeEach(async () => {
      const localVue = createLocalVue()
      const attachTo = createContainer()
      const propsData = { userId: '2000' }
      // Configure the local vue
      const core = Core.init(localVue).useAll()
      // Configure the core
      await core.configure()
      // Get router from core
      const { i18n, store, router } = core 
      // Finally, instanciate the component
      wrapper = mount(UserLink, { attachTo, localVue, propsData, i18n, store, router })
    })

    it('should build a link to the user profile', () => {
      const href = wrapper.attributes('href')
      expect(href).toBe('#/users/fatima/')
    })  
    
    it('should show the username by default', () => {
      const text = wrapper.text()
      expect(text).toBe('@fatima')
    })

    it('should show the display name instead of the username', async () => {
      await wrapper.setProps({ useDisplayName: true })
      const text = wrapper.text()
      expect(text).toBe('Fátima')
    })
  })

  describe('user link with slot, and username as "userId"', () => {
    let wrapper

    beforeEach(async () => {
      const localVue = createLocalVue()
      const attachTo = createContainer()
      const propsData = { userId: 'fatima' }
      // Configure the local vue
      const core = Core.init(localVue).useAll()
      // Configure the core
      await core.configure()
      // Get router from core
      const { i18n, store, router } = core
      const scopedSlots = { default: '<template slot-scope="{ user }">{{ user.email }}</template>'}
      // Finally, instanciate the component
      wrapper = mount(UserLink, { attachTo, localVue, propsData, i18n, store, router, scopedSlots })
    })

    it('should show the email instead of the username', () => {
      const text = wrapper.text()
      expect(text).toBe('engineering@icij.org')
    })
  })

  describe('disabled user link with an unknown user', () => {
    let wrapper

    beforeEach(async () => {
      const localVue = createLocalVue()
      const attachTo = createContainer()
      const propsData = { userId: 'edmond' }
      // Configure the local vue
      const core = Core.init(localVue).useAll()
      // Configure the core
      await core.configure()
      // Get router from core
      const { i18n, store, router } = core
      // Finally, instanciate the component
      wrapper = mount(UserLink, { attachTo, localVue, propsData, i18n, store, router })
    })

    it('should show nothing when the user is unknown', () => {
      const text = wrapper.text()
      expect(text).toBe('')
    })
  })
})
