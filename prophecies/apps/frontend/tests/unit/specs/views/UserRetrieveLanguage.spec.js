import {createLocalVue, mount} from '@vue/test-utils'

import '@/store'
import Core from '@/core'
import {server, rest} from '../../mocks/server'
import User from '@/models/User'

import UserRetrieveLanguage from '@/views/UserRetrieveLanguage'

describe('UserRetrieveLanguage', () => {
  let i18n
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
    const {wait, store, router} = core
    const stubs = ['router-link', 'app-waiter']
    const options = {
      i18n,
      localVue,
      store,
      stubs,
      router,
      wait
    }
    await core.configure()
    wrapper = mount(UserRetrieveLanguage, options)
    i18n = core['i18n']
  })

  afterEach(async () => {
    await wrapper.destroy()
  })

  it('should display language list', async () => {
    expect(wrapper.find('.user-retrieve-language__list').exists()).toBe(true)
  })

  it('should display the supported languages', async () => {
    const expected = ['English (EN)', 'Français (FR)', 'Español (ES)'];

    const languages = wrapper.findAll('.user-retrieve-language__list__language').wrappers

    expect(languages.length).toBe(expected.length)
    for (const language of languages) {
      expect(expected).toContain(language.text())
    }
  })

  it('should select English by default', async () => {
    expect(wrapper.vm.$i18n.locale).toBe('en')
    expect(wrapper.vm.$store.state.app.locale).toBe('en')
  })

  it('should change language when selecting French', async () => {
    expect(wrapper.vm.$i18n.locale).toBe('en')
    expect(wrapper.vm.$store.state.app.locale).toBe('en')

    wrapper.find('li[id="fr"]').trigger('click')
    await wrapper.vm.$nextTick()

    expect(wrapper.vm.locale).toBe('fr')
    expect(wrapper.vm.$store.state.app.locale).toBe('fr')
  })
})
