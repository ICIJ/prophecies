import { rest } from 'msw'

export default [
  rest.get('/api/v1/users', (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({
        data: [
          {
            type: 'User',
            id: 2,
            attributes: {
              url: 'http://localhost/api/v1/users/2/',
              first_name: 'Django',
              last_name: '',
              username: 'django',
              email: 'support@icij.org',
              email_md5: 'd159b514bfc6e718ac0a4ed0487d4d3e',
              is_staff: true
            },
            links: {
              self: 'http://localhost/api/v1/users/2/'
            }
          }
        ]
      })
    )
  }),

  rest.get('/api/v1/users/me', (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({
        data: {
          type: 'User',
          id: 2,
          attributes: {
            url: 'http://localhost/api/v1/users/2/',
            first_name: 'Django',
            last_name: '',
            username: 'django',
            email: 'support@icij.org',
            email_md5: 'd159b514bfc6e718ac0a4ed0487d4d3e',
            is_staff: true
          },
          links: {
            self: 'http://localhost/api/v1/users/2/'
          }
        }
      })
    )
  })
]
