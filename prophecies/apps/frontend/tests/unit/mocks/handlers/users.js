import { rest } from 'msw'

export default [
  rest.get('/api/v1/users', (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({
        data: [
          {
            type: 'User',
            id: '1',
            attributes: {
              firstName: '',
              lastName: '',
              username: 'olivia',
              email: '',
              emailMd5: 'd41d8cd98f00b204e9800998ecf8427e',
              isStaff: true
            },
            links: {
              self: 'http://localhost:9009/api/v1/users/1/'
            }
          },
          {
            type: 'User',
            id: '2',
            attributes: {
              url: 'http://localhost/api/v1/users/2/',
              firstName: 'Django',
              lastName: '',
              username: 'django',
              email: 'support@icij.org',
              emailMd5: 'd159b514bfc6e718ac0a4ed0487d4d3e',
              isStaff: true
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
          id: '2',
          attributes: {
            url: 'http://localhost/api/v1/users/2/',
            firstName: 'Django',
            lastName: '',
            username: 'django',
            email: 'support@icij.org',
            emailMd5: 'd159b514bfc6e718ac0a4ed0487d4d3e',
            isStaff: true
          },
          links: {
            self: 'http://localhost/api/v1/users/2/'
          }
        }
      })
    )
  })
]
