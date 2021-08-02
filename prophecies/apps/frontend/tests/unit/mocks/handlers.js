// src/mocks/handlers.js
import { rest } from 'msw'

export const handlers = [

  rest.get('/api/v1/settings', (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json([
        {
          key: 'appName',
          value: 'Data Fact Check'
        },
        {
          key: 'orgName',
          value: 'ICIJ.org'
        },
        {
          key: 'appVersion',
          value: '0.4.6'
        }
      ])
    )
  }),

  rest.get('/api/v1/users', (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json([
        {
          id: 2,
          url: 'http://0.0.0.0:8008/api/v1/users/2/',
          first_name: 'Django',
          last_name: '',
          username: 'django',
          email: 'support@icij.org',
          email_md5: 'd159b514bfc6e718ac0a4ed0487d4d3e',
          is_staff: true
        }
      ])
    )
  }),

  rest.get('/api/v1/users/me.json', (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({
        id: 2,
        url: 'http://0.0.0.0:8008/api/v1/users/2/',
        first_name: 'Django',
        last_name: '',
        username: 'django',
        email: 'support@icij.org',
        email_md5: 'd159b514bfc6e718ac0a4ed0487d4d3e',
        is_staff: true
      })
    )
  })
]
