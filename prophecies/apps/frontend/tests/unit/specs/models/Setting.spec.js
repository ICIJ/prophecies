import '@/store'
import {rest, server} from '../../mocks/server'
import Setting from '@/models/Setting'

describe('Setting', () => {
  beforeAll(() => {
    Setting.deleteAll()
  })

  afterEach(() => {
    Setting.deleteAll()
    server.resetHandlers()
  })

  it('should return a list of settings', async () => {
    server.use(rest.get('/api/v1/settings', (req, res, ctx) => {
      return res.once(ctx.json({
        data: [
          {type: 'Setting', id: '1', attributes: {key: 'foo', value: 1}},
          {type: 'Setting', id: '2', attributes: {key: 'bar', value: 2}}
        ]
      }))
    }))
    await Setting.api().get()
    expect(Setting.all()).toHaveLength(2)
    expect(Setting.query().where('key', 'foo').first().value).toBe(1)
    expect(Setting.query().where('key', 'bar').first().value).toBe(2)
  })

  describe('`allAsObject` static method', () => {
    it('should return an object with all values', async () => {
      server.use(rest.get('/api/v1/settings', (req, res, ctx) => {
        return res.once(ctx.json({
          data: [
            {type: 'Setting', id: '1', attributes: {key: 'foo', value: 1}},
            {type: 'Setting', id: '2', attributes: {key: 'bar', value: 2}}
          ]
        }))
      }))
      await Setting.api().get()
      const settings = Setting.allAsObject()
      expect(settings.foo).toBe(1)
      expect(settings.bar).toBe(2)
    })

    it('should convert key to camelCase', async () => {
      server.use(rest.get('/api/v1/settings', (req, res, ctx) => {
        return res.once(ctx.json({
          data: [
            {type: 'Setting', id: '1', attributes: {key: 'org_name', value: 'ICIJ'}},
            {type: 'Setting', id: '2', attributes: {key: 'app_name', value: 'Prophecies'}}
          ]
        }))
      }))
      await Setting.api().get()
      const settings = Setting.allAsObject()
      expect(settings.orgName).toBe('ICIJ')
      expect(settings.appName).toBe('Prophecies')
    })
  })
})
