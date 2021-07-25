import '@/store'
import axios from 'axios'
import User from '@/models/User'

const spyAxiosRequest = jest.spyOn(axios, 'request').mockResolvedValue({ data: [] })

describe('User', () => {
  beforeEach(() => {
    User.deleteAll()
    spyAxiosRequest.mockClear()
  })

  afterAll(() => {
    spyAxiosRequest.mockRestore()
  })

  it('should call the /api/v1/users/ endpoint', async () => {
    await User.api().get()
    const callArguments = expect.objectContaining({ method: 'get', baseURL: '/api/v1/users/' })
    expect(spyAxiosRequest).toHaveBeenCalledWith(callArguments)
  })

  it('should return a User instance', async () => {
    spyAxiosRequest.mockResolvedValue({ data: { id: 18, username: 'foo' } })
    await User.api().get(18)
    expect(User.find(18)).toBeInstanceOf(User)
    expect(User.find(18).id).toBe(18)
  })

  describe('`me` static method', () => {
    it('should call the /api/v1/users/me.json endpoint', async () => {
      await User.api().me()
      const callArguments = expect.objectContaining({ method: 'get', baseURL: '/api/v1/users/', url: 'me.json' })
      expect(spyAxiosRequest).toHaveBeenCalledWith(callArguments)
    })

    it('should return a User instance', async () => {
      spyAxiosRequest.mockResolvedValue({ data: { id: 20, username: 'bar' } })
      await User.api().me()
      expect(User.me()).toBeInstanceOf(User)
      expect(User.me().id).toBe(20)
    })

    it('should return null when user is not loaded yet', async () => {
      expect(User.me()).toBe(null)
    })

    it('should return null when user cannot be loaded', async () => {
      spyAxiosRequest.mockRejectedValue(new Error({ status: 403 }))
      await expect(User.api().me()).rejects.toBeInstanceOf(Error)
      expect(User.me()).toBe(null)
    })
  })
})
