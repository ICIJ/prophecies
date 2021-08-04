import { rest } from 'msw'

export default [
  rest.get('/api/v1/settings', (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({
        data: [
          {
            type: 'Setting',
            attributes: {
              key: 'appName',
              value: 'Data Fact Check'
            }
          },
          {
            type: 'Setting',
            attributes: {
              key: 'orgName',
              value: 'ICIJ.org'
            }
          },
          {
            type: 'Setting',
            attributes: {
              key: 'appVersion',
              value: '0.4.6'
            }
          }
        ]
      })
    )
  })
]
