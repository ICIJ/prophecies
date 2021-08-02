import '@/store'
import { server, rest } from '../../mocks/server'
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
    const settings = [{ key: 'foo', value: 1 }, { key: 'bar', value: 2 }]
    server.use(rest.get('/api/v1/settings', (req, res, ctx) => res.once(ctx.json(settings))))
    await Setting.api().get()
    expect(Setting.all()).toHaveLength(2)
    expect(Setting.query().where('key', 'foo').first().value).toBe(1)
    expect(Setting.query().where('key', 'bar').first().value).toBe(2)
  })

  describe('`allAsObject` static method', () => {
    it('should return an object with all values', async () => {
      const data = [{ key: 'foo', value: 1 }, { key: 'bar', value: 2 }]
      server.use(rest.get('/api/v1/settings', (req, res, ctx) => res.once(ctx.json(data))))
      await Setting.api().get()
      const settings = Setting.allAsObject()
      expect(settings.foo).toBe(1)
      expect(settings.bar).toBe(2)
    })

    it('should convert key to camelCase', async () => {
      const data = [{ key: 'org_name', value: 'ICIJ' }, { key: 'app_name', value: 'Prophecies' }]
      server.use(rest.get('/api/v1/settings', (req, res, ctx) => res.once(ctx.json(data))))
      await Setting.api().get()
      const settings = Setting.allAsObject()
      expect(settings.orgName).toBe('ICIJ')
      expect(settings.appName).toBe('Prophecies')
    })
  })
})
