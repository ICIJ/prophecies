import {createLocalVue} from '@vue/test-utils'

import {server, rest} from '../../mocks/server'
import {Core} from '@/core'
import User from '@/models/User'

// Mock the router's configuration
jest.mock('@/router', () => ({
  routes: [
    {
      name: 'home',
      path: '/'
    },
    {
      name: 'dashboard',
      path: '/dashboard'
    },
    {
      name: 'login',
      path: '/login'
    },
    {
      name: 'error',
      path: '/error'
    }
  ]
}))

describe('router/guards', () => {
  const {localVue} = createLocalVue()
  let core

  beforeEach(async () => {
    // Create a core instance
    core = Core.init(localVue).useRouter()
  })

  afterAll(() => {
    User.deleteAll()
    server.resetHandlers()
  })

  it('should redirect to "login" if the user is not authenticated', async () => {
    // Mock reject promise for the user endpoint
    server.use(rest.get('/api/v1/users/me/', (req, res, ctx) => res(ctx.status(403))))
    // The navigation is going to throw an exception
    await expect(core.router.push({name: 'dashboard'})).rejects.toBeInstanceOf(Error)
    // The router should now be on the login page
    expect(core.router.currentRoute.name).toBe('login')
  })

  it('should not redirect to "login" when user is not authenticated but heading to "login"', async () => {
    // Mock reject promise for the user endpoint
    server.use(rest.get('/api/v1/users/me/', (req, res, ctx) => res(ctx.status(403))))
    // The navigation is not going to throw an exception
    await core.router.push({name: 'login'})
    // The router should now be on the login page
    expect(core.router.currentRoute.name).toBe('login')
  })

  it('should not redirect to "login" when user is not authenticated but heading to "error"', async () => {
    // Mock reject promise for the user endpoint
    server.use(rest.get('/api/v1/users/me/', (req, res, ctx) => res(ctx.status(403))))
    // The navigation is not going to throw an exception
    await core.router.push({name: 'error'})
    // The router should now be on the error page
    expect(core.router.currentRoute.name).toBe('error')
  })

  it('should not redirect to "login" if the user is authenticated', async () => {
    const me = {data: {id: 20, username: 'bar'}}
    server.use(rest.get('/api/v1/users/me/', (req, res, ctx) => res.once(ctx.json(me))))
    // The navigation is not going to throw an exception
    await core.router.push({name: 'dashboard'})
    // The router should now be on the dashboard page
    expect(core.router.currentRoute.name).toBe('dashboard')
  })
})
