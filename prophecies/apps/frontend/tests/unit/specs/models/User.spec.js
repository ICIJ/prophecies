import axios from 'axios'
import store from '@/store'
import User from '@/models/User'

const spyAxiosRequest = jest.spyOn(axios, 'request').mockResolvedValue({ data: [] })

describe('User', () => {
  beforeEach(() => {
    store.dispatch('entities/deleteAll')
  })

  it('should call the /api/v1/users/ endpoint', async () => {
    await User.api().get()
    const callArguments = expect.objectContaining({ method: 'get', baseURL: '/api/v1/users/' })
    expect(spyAxiosRequest).toHaveBeenCalledWith(callArguments)
  })

  describe('`me` static method', () => {
    it('should call the /api/v1/users/me.json endpoint', async () => {
      await User.api().me()
      const callArguments = expect.objectContaining({ method: 'get', baseURL: '/api/v1/users/', url: 'me.json' })
      expect(spyAxiosRequest).toHaveBeenCalledWith(callArguments)
    })

    it('should return a User instance', async () => {
      await User.api().me()
      expect(User.me()).toBeInstanceOf(User)
    })

    it('should return null when user is not loaded yet', async () => {
      expect(User.me()).toBe(null)
    })
  })
})
