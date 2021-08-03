import '@/store'
import { server, rest } from '../../mocks/server'
import User from '@/models/User'

describe('User', () => {
  describe('`me` static method', () => {
    beforeAll(() => {
      User.deleteAll()
    })

    afterEach(() => {
      User.deleteAll()
      server.resetHandlers()
    })

    it('should return a User instance', async () => {
      server.use(rest.get('/api/v1/users/me/', (req, res, ctx) => {
        return res.once(ctx.json({
          data: {
            id: 20,
            attributes: {
              username: 'bar'
            }
          }
        }))
      }))
      await User.api().me()
      expect(User.me()).toBeInstanceOf(User)
      expect(User.me().id).toBe(20)
    })

    it('should return null when user is not loaded yet', async () => {
      expect(User.me()).toBe(null)
    })

    it('should return null when user cannot be loaded', async () => {
      server.use(rest.get('/api/v1/users/me/', (req, res, ctx) => res(ctx.status(403))))
      await expect(User.api().me()).rejects.toBeInstanceOf(Error)
      expect(User.me()).toBe(null)
    })
  })
})
