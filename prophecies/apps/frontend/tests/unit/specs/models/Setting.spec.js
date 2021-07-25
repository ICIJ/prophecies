import axios from 'axios'
import store from '@/store'
import Setting from '@/models/Setting'

const spyAxiosRequest = jest.spyOn(axios, 'request').mockResolvedValue({ data: [] })

describe('Setting', () => {
  beforeEach(() => {
    store.dispatch('entities/deleteAll')
    spyAxiosRequest.mockClear()
  })

  afterAll(() => {
    spyAxiosRequest.mockRestore()
  })

  it('should call the /api/v1/settings/ endpoint', async () => {
    await Setting.api().get()
    const callArguments = expect.objectContaining({ method: 'get', baseURL: '/api/v1/settings/' })
    expect(spyAxiosRequest).toHaveBeenCalledWith(callArguments)
  })

  it('should returns a list of settings', async () => {
    const data = [{ key: 'foo', value: 1 }, { key: 'bar', value: 2 }]
    spyAxiosRequest.mockResolvedValue({ data })
    await Setting.api().get()
    expect(Setting.all()).toHaveLength(2)
    expect(Setting.query().where('key', 'foo').first().value).toBe(1)
    expect(Setting.query().where('key', 'bar').first().value).toBe(2)
  })

  describe('`allAsObject` static method', () => {
    it('should returns an object with all values', async () => {
      const data = [{ key: 'foo', value: 1 }, { key: 'bar', value: 2 }]
      spyAxiosRequest.mockResolvedValue({ data })
      await Setting.api().get()
      const settings = Setting.allAsObject()
      expect(settings.foo).toBe(1)
      expect(settings.bar).toBe(2)
    })

    it('should convert key to camelCase', async () => {
      const data = [{ key: 'org_name', value: 'ICIJ' }, { key: 'app_name', value: 'Prophecies' }]
      spyAxiosRequest.mockResolvedValue({ data })
      await Setting.api().get()
      const settings = Setting.allAsObject()
      expect(settings.orgName).toBe('ICIJ')
      expect(settings.appName).toBe('Prophecies')
    })
  })
})
